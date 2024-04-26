from dataclasses import replace
from typing import Optional, Tuple

from datasphere.api import jobs_pb2 as jobs
from datasphere.config import Config, Environment, VariablePath, parse_docker_image, parse_working_storage
from datasphere.files import prepare_inputs
from datasphere.validation import validate_paths


def fork_params(args, source_params: jobs.JobParameters, tmpdir) -> Config:
    var_to_old_input = {
        f.desc.var: VariablePath(path=f.desc.path, var=f.desc.var)
        for f in source_params.input_files
        if f.desc.var
    }
    var_to_old_output = {
        f.var: VariablePath(path=f.path, var=f.var)
        for f in source_params.output_files
        if f.var
    }

    new_inputs = []
    new_outputs = []
    new_vars = set()
    for v in args.var or []:
        var, path = parse_name_value(v)
        var_path = VariablePath(var=var, path=path)
        new_vars.add(var)
        if var in var_to_old_input:
            new_inputs.append(var_path)
        elif var in var_to_old_output:
            new_outputs.append(var_path)
        else:
            raise ValueError(f'No variable path in source job: {var}')

    # Environment override details:
    # - Docker image from source job can only be changed, but not reset, so it's ok to pass `None` as docker image
    #   even if source job has some docker image.
    # - Python env cannot be modified.
    # - Environment variables, if set, substitute source job ones.
    env = Environment(vars=None, docker_image=None, python=None)
    if args.env_var:
        env.vars = {
            name: value for name, value in
            [parse_name_value(v) for v in args.env_var]
        }
    env.docker_image = parse_docker_image(get_docker_dict_from_args(args))

    working_storage = parse_working_storage(get_working_storage_dict_from_args(args))

    # All parameters which cannot be overridden are left with their default values.
    cfg = Config(
        cmd='',
        inputs=new_inputs,
        outputs=new_outputs,
        s3_mounts=[],
        datasets=[],
        env=env,
        cloud_instance_type=args.cloud_instance_type or '',
        attach_project_disk=False,
        content='',
        working_storage=working_storage,
        name=args.name,
        desc=args.desc,
    )

    # We need to check all paths on overlaps – overridden and source ones.
    old_inputs = [old_input for var, old_input in var_to_old_input.items() if var not in new_vars]
    old_outputs = [old_output for var, old_output in var_to_old_output.items() if var not in new_vars]
    cfg_joint_io = replace(cfg, inputs=new_inputs + old_inputs, outputs=new_outputs + old_outputs)
    validate_paths(cfg_joint_io, py_env=None)

    cfg.inputs = prepare_inputs(cfg.inputs, tmpdir)

    return cfg


def get_docker_dict_from_args(args) -> Optional[dict]:
    if args.docker_image_id or args.docker_image_url:
        if args.docker_image_id and args.docker_image_url:
            raise ValueError('For docker image, specify either ID or URL')
        if args.docker_image_id:
            return {'docker': args.docker_image_id}
        else:
            data = {'image': args.docker_image_url}
            if args.docker_image_username:
                data['username'] = args.docker_image_username
            if args.docker_image_password_secret_id:
                data['password'] = {'secret-id': args.docker_image_password_secret_id}
            return {'docker': data}
    return {}


def get_working_storage_dict_from_args(args) -> Optional[dict]:
    if args.working_storage_type or args.working_storage_size:
        d = {}
        if args.working_storage_type:
            d['type'] = args.working_storage_type
        if args.working_storage_size:
            d['size'] = args.working_storage_size
        return {'working-storage': d}
    return {}


def parse_name_value(s: str) -> Tuple[str, str]:
    # split by first `=` since it cannot be in path var or env var
    parts = s.split('=', 1)
    if len(parts) != 2:
        raise ValueError(f'Invalid name-value pair: {s}')
    return parts[0], parts[1]
