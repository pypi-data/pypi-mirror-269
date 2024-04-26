import re
from dataclasses import dataclass, field
from pytest import raises
from typing import List, Optional

from datasphere.api import jobs_pb2 as jobs
from datasphere.config import VariablePath, Config, Environment, DockerImage, Password
from datasphere.fork import (
    fork_params,
    get_docker_dict_from_args,
    get_working_storage_dict_from_args,
    parse_name_value,
)


@dataclass
class Args:
    var: List[str] = field(default_factory=list)
    env_var: List[str] = field(default_factory=list)
    docker_image_id: Optional[str] = None
    docker_image_url: Optional[str] = None
    docker_image_username: Optional[str] = None
    docker_image_password_secret_id: Optional[str] = None
    working_storage_type: Optional[str] = None
    working_storage_size: Optional[str] = None
    cloud_instance_type: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None


def test_fork_params(tmp_path):
    source_input_1 = tmp_path / 'source_input_1.txt'
    source_input_1.write_text('source input 1')
    source_input_2 = tmp_path / 'in' / 'source_input_2.txt'
    source_input_2.parent.mkdir()
    source_input_2.write_text('source input 2')
    source_input_3 = tmp_path / 'source_input_3.txt'
    source_input_3.write_text('source input 3')
    source_output_1 = 'out'
    source_output_2 = 'source_output_2.txt'

    source_params = jobs.JobParameters(
        input_files=[
            VariablePath(str(source_input_1), var='INPUT1').get_file(),
            VariablePath(str(source_input_2), var='INPUT2').get_file(),
            VariablePath(str(source_input_3), var='INPUT3').get_file(),
        ],
        output_files=[
            VariablePath(source_output_1, var='OUTPUT1').file_desc,
            VariablePath(source_output_2, var='OUTPUT2').file_desc,
        ]
    )

    new_input_1 = tmp_path / 'new_in'
    new_input_1.mkdir()
    new_input_1_inner_file = new_input_1 / 'new_input_1.txt'
    new_input_1_inner_file.write_text('new input 1')
    new_input_1_overlaps_old = tmp_path / 'in'
    new_input_3 = tmp_path / 'source_input_3.txt'  # even if path matches old one, new file content will be sent
    new_input_3.write_text('new input 3')
    new_output_2_overlaps_old = 'out/new_output_1.txt'
    new_output_2 = 'new_output_2.txt'

    def get_cfg(
            inputs: Optional[List[VariablePath]] = None,
            outputs: Optional[List[VariablePath]] = None,
            env: Optional[Environment] = None,
            cloud_instance_type: Optional[str] = None,
            name: Optional[str] = None,
            desc: Optional[str] = None,
            working_storage: Optional[jobs.ExtendedWorkingStorage] = None,
    ) -> Config:
        return Config(
            cmd='',
            inputs=inputs or [],
            outputs=outputs or [],
            s3_mounts=[],
            datasets=[],
            env=env or Environment(vars=None, docker_image=None, python=None),
            cloud_instance_type=cloud_instance_type or '',
            attach_project_disk=False,
            content='',
            name=name,
            desc=desc,
            working_storage=working_storage,
        )

    for args, expected_cfg, expected_err in (
            (Args(var=['INPUT1=foo.txt', 'FOO=bar.txt']), None, 'No variable path in source job: FOO'),
            (Args(working_storage_type='DDT'), None, 'possible working storage types are: [SSD]'),
            (Args(env_var=['FOO']), None, 'Invalid name-value pair: FOO'),
            (Args(var=[f'INPUT1={new_input_1_overlaps_old}']), None, f"Path '{tmp_path}/in/source_input_2.txt' is included in path '{tmp_path}/in'"),
            (Args(var=[f'OUTPUT2={new_output_2_overlaps_old}']), None, "Path 'out/new_output_1.txt' is included in path 'out'"),
            (Args(), get_cfg(), None),
            (
                    Args(docker_image_id='b3p16de49mh0f9khpar3'),
                    get_cfg(env=Environment(vars=None, docker_image='b3p16de49mh0f9khpar3', python=None)),
                    None,
            ),
            (
                    Args(
                        var=[f'INPUT1={str(new_input_1)}', f'INPUT3={str(new_input_3)}', f'OUTPUT2={new_output_2}'],
                        env_var=['FOO=fjdiw=39m', 'BAR=777'],
                        docker_image_url='cr.yandex/foo/bar:latest',
                        docker_image_username='user',
                        docker_image_password_secret_id='my-secret',
                        working_storage_type='SSD',
                        working_storage_size='3Tb',
                        cloud_instance_type='g2.8',
                    ),
                    get_cfg(
                        inputs=[
                            VariablePath(path=str(new_input_1), var='INPUT1', compression_type=jobs.FileCompressionType.ZIP),
                            VariablePath(path=str(new_input_3), var='INPUT3'),
                        ],
                        outputs=[
                            VariablePath(path=new_output_2, var='OUTPUT2'),
                        ],
                        env=Environment(
                            vars={'FOO': 'fjdiw=39m', 'BAR': '777'},
                            docker_image=DockerImage(
                                url='cr.yandex/foo/bar:latest',
                                username='user',
                                password=Password(text='my-secret', is_secret=True),
                            ),
                            python=None,
                        ),
                        cloud_instance_type='g2.8',
                        working_storage=jobs.ExtendedWorkingStorage(
                            type=jobs.ExtendedWorkingStorage.StorageType.SSD,
                            size_gb=3072,
                        )
                    ),
                    None,
            ),
    ):
        if expected_err:
            with raises(ValueError, match=re.escape(expected_err)):
                fork_params(args, source_params, tmp_path)
        else:
            actual_cfg = fork_params(args, source_params, tmp_path)

            # Lazy attrs `_file`, `_archive_path` are hard to test, so we drop it from actual config.
            for f in actual_cfg.inputs:
                f._file = None
                f._archive_path = None

            assert actual_cfg == expected_cfg


def test_get_docker_dict_from_args():
    for args, expected_dict in (
            (Args(), {}),
            (Args(docker_image_id='b3p16de49mh0f9khpar3'), {'docker': 'b3p16de49mh0f9khpar3'}),
            (
                    Args(docker_image_url='cr.yandex/foo/bar:latest'),
                    {'docker': {'image': 'cr.yandex/foo/bar:latest'}}
            ),
            (
                    Args(
                        docker_image_url='cr.yandex/foo/bar:latest',
                        docker_image_username='user',
                        docker_image_password_secret_id='my-secret',
                    ),
                    {'docker': {
                        'image': 'cr.yandex/foo/bar:latest',
                        'username': 'user',
                        'password': {'secret-id': 'my-secret'}
                    }}
            )
    ):
        assert get_docker_dict_from_args(args) == expected_dict

    with raises(ValueError, match='For docker image, specify either ID or URL'):
        get_docker_dict_from_args(Args(docker_image_id='id', docker_image_url='url'))


def test_get_working_storage_dict_from_args():
    for args, expected_dict in (
            (Args(), {}),
            (Args(working_storage_type='SSD'), {'working-storage': {'type': 'SSD'}}),
            (Args(working_storage_size='30Gb'), {'working-storage': {'size': '30Gb'}}),
            (
                    Args(working_storage_type='SSD', working_storage_size='30Gb'),
                    {'working-storage': {'size': '30Gb', 'type': 'SSD'}},
            ),
    ):
        assert get_working_storage_dict_from_args(args) == expected_dict


def test_parse_name_value():
    assert parse_name_value('NAME=skf=238v=3si') == ('NAME', 'skf=238v=3si')
    assert parse_name_value('NAME=') == ('NAME', '')
    with raises(ValueError, match='Invalid name-value pair: NAME'):
        parse_name_value('NAME')
