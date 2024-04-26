import argparse
from datetime import datetime, timedelta
import sys
import grpc
import logging
import os
from pathlib import Path
import tempfile

from datasphere.auth import oauth_token_env_var_1, oauth_token_env_var_2
from datasphere.client import Client, OperationError, ProgramError
from datasphere.config import parse_config, check_limits
from datasphere.files import prepare_inputs, prepare_local_modules
from datasphere.fork import fork_params
from datasphere.logs import configure_logging
from datasphere.output import output, job_spec, project_spec, Format, ExecutionData, execution_data_spec
from datasphere.pyenv import define_py_env
from datasphere.utils import check_package_version, print_logs_files
from datasphere.validation import validate_paths
from datasphere.version import version

logger = logging.getLogger('datasphere.main')
# logger for things which do not go through logging, such as traceback in stderr
logger_file = logging.getLogger('datasphere_file')


def execute(args):
    cfg = parse_config(args.config)

    py_env = None
    if cfg.env.python:
        logger.debug('defining python env ...')
        py_env = define_py_env(cfg.python_root_modules, cfg.env.python)

    validate_paths(cfg, py_env)

    async_mode = args.async_

    with tempfile.TemporaryDirectory(prefix='datasphere_') as tmpdir:
        logger.debug('using tmp dir `%s` to prepare local files', tmpdir)

        cfg.inputs = prepare_inputs(cfg.inputs, tmpdir)

        if py_env:
            local_modules = [f.get_file() for f in prepare_local_modules(py_env, tmpdir)]
            # Preserve original local modules paths (before archiving).
            sha256_to_display_path = {f.sha256: p for f, p in zip(local_modules, py_env.local_modules_paths)}
        else:
            local_modules = []
            sha256_to_display_path = {}

        check_limits(cfg, local_modules)

        job_params = cfg.get_job_params(py_env, local_modules)
        if py_env:
            logger.debug('resulting conda.yaml:\n%s', job_params.env.python_env.conda_yaml)

        client = get_client(args)

        job_id = client.create(job_params, cfg, args.project_id, sha256_to_display_path)
        op, execute_call = client.execute(job_id, async_mode=async_mode)
        logger.debug('operation `%s` executes the job', op.id)

    if not async_mode:
        client.wait_for_completion(op, execute_call)
    elif args.output != sys.stdout:
        output([ExecutionData(job_id=job_id, operation_id=op.id)], execution_data_spec, args.output, Format.JSON)


def fork(args):
    async_mode = args.async_

    client = get_client(args)

    source_job_id = args.id
    source_job = client.get(source_job_id)

    if source_job.data_expires_at:
        now = datetime.now()
        data_expires_at = source_job.data_expires_at.ToDatetime()
        if now > data_expires_at:
            logger.warning('source job data is already expired')
        elif data_expires_at - now < timedelta(days=3):
            logger.warning('source job data will expire after %s', now - data_expires_at)

    source_params = source_job.job_parameters

    with tempfile.TemporaryDirectory(prefix='datasphere_') as tmpdir:
        logger.debug('using tmp dir `%s` to prepare local files', tmpdir)
        cfg_overrides = fork_params(args, source_params, tmpdir)
        check_limits(cfg_overrides, local_modules=[])
        job_id = client.clone(source_job_id, cfg_overrides)
        op, execute_call = client.execute(job_id, async_mode=async_mode)
        logger.debug('operation `%s` executes the job', op.id)

    if not async_mode:
        client.wait_for_completion(op, execute_call)
    elif args.output != sys.stdout:
        output([ExecutionData(job_id=job_id, operation_id=op.id)], execution_data_spec, args.output, Format.JSON)


def attach(args):
    client = get_client(args)
    op, execute_call = client.execute(args.id, std_logs_offset=-1)
    client.wait_for_completion(op, execute_call)


def ls(args):
    client = get_client(args)
    jobs = client.list(args.project_id)
    output(jobs, job_spec, args.output, args.format)


def get(args):
    client = get_client(args)
    job = client.get(args.id)
    output([job], job_spec, args.output, args.format)


def delete(args):
    client = get_client(args)
    client.delete(args.id)
    logger.info('job deleted')


def cancel(args):
    client = get_client(args)
    client.cancel(args.id)


def set_data_ttl(args):
    client = get_client(args)
    if args.days < 1:
        raise ValueError('TTL days should be positive')
    client.set_data_ttl(args.id, args.days)


def ls_projects(args):
    client = get_client(args)
    projects = client.list_projects(args.community_id)
    output(projects, project_spec, args.output, args.format)


def get_project(args):
    client = get_client(args)
    project = client.get_project(args.id)
    output([project], project_spec, args.output, args.format)


def show_version(_):
    print(version)


def show_changelog(_):
    print(Path(__file__).with_name('changelog.md').read_text())


def get_client(args):
    return Client(args.token, args.profile)


def build_arg_parser() -> argparse.ArgumentParser:
    parser_datasphere = argparse.ArgumentParser(prog='datasphere')
    parser_datasphere.add_argument(
        '-t', '--token',
        default=os.environ.get(oauth_token_env_var_1) or os.environ.get(oauth_token_env_var_2),
        help='YC OAuth token, see https://cloud.yandex.com/docs/iam/concepts/authorization/oauth-token'
    )
    parser_datasphere.add_argument(
        '-l', '--log-level', default=logging.INFO,
        choices=[logging.getLevelName(level) for level in (logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG)],
        help='Logging level',
    )
    parser_datasphere.add_argument(
        '--log-config', type=argparse.FileType('r'), help='Custom logging config'
    )
    parser_datasphere.add_argument('--log-dir', help='Logs directory (temporary directory by default)')
    parser_datasphere.add_argument('--profile', help='`yc` utility profile')
    subparsers_datasphere = parser_datasphere.add_subparsers(required=True)

    parser_version = subparsers_datasphere.add_parser('version', help='Show version')
    parser_version.set_defaults(func=show_version)

    parser_changelog = subparsers_datasphere.add_parser('changelog', help='Show changelog')
    parser_changelog.set_defaults(func=show_changelog)

    parser_project = subparsers_datasphere.add_parser('project')
    subparsers_project = parser_project.add_subparsers(required=True)

    parser_job = subparsers_project.add_parser('job')
    subparsers_job = parser_job.add_subparsers(required=True)

    def add_project_id_argument(parser):
        parser.add_argument('-p', '--project-id', required=True, help='DataSphere project ID')

    def add_id_argument(parser, help: str = 'Job ID'):
        parser.add_argument('--id', required=True, help=help)

    def add_output_argument(parser, help: str = 'Output file (stdout by default)'):
        parser.add_argument('-o', '--output', help=help, default=sys.stdout, type=argparse.FileType('w'))

    def add_format_argument(parser):
        parser.add_argument(
            '--format', help='Output format',
            choices=[e.value for e in Format],
            default=Format.TABLE.value,
        )

    def add_async_argument(parser):
        parser.add_argument('--async', action='store_true', dest='async_', help='Async mode')

    async_execution_output_help = 'File with execution data, for async mode (none by default)'

    parser_execute = subparsers_job.add_parser('execute', help='Execute job')
    add_project_id_argument(parser_execute)
    parser_execute.add_argument('-c', '--config', required=True, help='Config file', type=argparse.FileType('r'))
    add_async_argument(parser_execute)
    add_output_argument(parser_execute, help=async_execution_output_help)
    parser_execute.set_defaults(func=execute)

    parser_fork = subparsers_job.add_parser('fork', help='Execute job using existing one as a template')
    add_id_argument(parser_fork, help='Source job ID')
    parser_fork.add_argument('--var', action='append', help='New path for variable', metavar='NAME=PATH')
    parser_fork.add_argument('--name', help='New job name')
    parser_fork.add_argument('--desc', help='New job description')
    parser_fork.add_argument('--env-var', action='append', help='Environment variable', metavar='NAME=VALUE')
    parser_fork.add_argument('--docker-image-id', help='ID of Docker image resource')
    parser_fork.add_argument('--docker-image-url', help='URL of Docker image')
    parser_fork.add_argument('--docker-image-username', help='Username for Docker image')
    parser_fork.add_argument('--docker-image-password-secret-id', help='Secret name of password for Docker image')
    parser_fork.add_argument('--working-storage-type', help='Working storage disk type')
    parser_fork.add_argument('--working-storage-size', help='Working storage disk size')
    parser_fork.add_argument('--cloud-instance-type', help='Computing resource configuration for executing the job')
    add_async_argument(parser_fork)
    add_output_argument(parser_fork, help=async_execution_output_help)
    parser_fork.set_defaults(func=fork)

    parser_attach = subparsers_job.add_parser('attach', help='Attach to the job execution')
    add_id_argument(parser_attach)
    parser_attach.set_defaults(func=attach)

    parser_list = subparsers_job.add_parser('list', help='List jobs')
    add_project_id_argument(parser_list)
    add_output_argument(parser_list)
    add_format_argument(parser_list)
    parser_list.set_defaults(func=ls)

    parser_get = subparsers_job.add_parser('get', help='Get job')
    add_id_argument(parser_get)
    add_output_argument(parser_get)
    add_format_argument(parser_get)
    parser_get.set_defaults(func=get)

    parser_delete = subparsers_job.add_parser('delete', help='Delete job')
    add_id_argument(parser_delete)
    # parser_delete.set_defaults(func=delete)  # DATASPHERE-1339

    parser_cancel = subparsers_job.add_parser('cancel', help='Cancel job')
    add_id_argument(parser_cancel)
    parser_cancel.set_defaults(func=cancel)

    parser_project_get = subparsers_project.add_parser('get', help='Get project')
    add_id_argument(parser_project_get, help='Project ID')
    add_output_argument(parser_project_get)
    add_format_argument(parser_project_get)
    parser_project_get.set_defaults(func=get_project)

    parser_project_list = subparsers_project.add_parser('list', help='List projects')
    parser_project_list.add_argument('-c', '--community-id', required=True, help='Community ID')
    add_output_argument(parser_project_list)
    add_format_argument(parser_project_list)
    parser_project_list.set_defaults(func=ls_projects)

    parser_set_data_ttl = subparsers_job.add_parser('set-data-ttl', help='Set job data TTL')
    add_id_argument(parser_set_data_ttl)
    # maybe we need argument with some string timedelta format, i.e. "1y100d10h" (1 year, 100 days and 10 hours)
    parser_set_data_ttl.add_argument('--days', required=True, help='Data TTL (days)', type=int)
    parser_set_data_ttl.set_defaults(func=set_data_ttl)

    return parser_datasphere


def main():
    arg_parser = build_arg_parser()

    args = arg_parser.parse_args()

    logs_file_path = configure_logging(args.log_level, args.log_config, args.log_dir)
    logger.info('logs file path: %s', logs_file_path)

    try:
        args.func(args)
    except Exception as e:
        log_exception(e, logs_file_path)
        print_logs_files(logs_file_path)
        raise
    finally:
        check_package_version()


def log_exception(e: Exception, logs_file_path: str):
    title = 'Error occurred'
    md = None
    if isinstance(e, grpc.RpcError):
        md = e.args[0].initial_metadata
        title = 'RPC error occurred'
    elif isinstance(e, OperationError):
        md = e.call_which_created_op.initial_metadata()
        title = 'Operation error occurred'
    elif isinstance(e, ProgramError):
        title = 'Program error occurred'
    md_str = '\n\theaders\n' + '\n'.join(f'\t\t{h.key}: {h.value}' for h in md) if md else ''
    logger.error('%s\n\tlogs file path: %s%s', title, logs_file_path, md_str)
    logger_file.exception(e)


if __name__ == '__main__':
    main()
