from pathlib import Path
from typing import List, Set, Optional

from datasphere.config import Config
from datasphere.pyenv import PythonEnv


def _check_paths_do_not_contain_parents(paths: List[Path]) -> None:
    if len(paths) < 2:
        return
    unique_paths: Set[Path] = set(paths)
    if len(paths) != len(unique_paths):
        raise ValueError('Paths must be unique')
    for path in unique_paths:
        for parent in path.parents:
            if parent in unique_paths:
                raise ValueError(f"Path '{path}' is included in path '{parent}'")


def validate_inputs(config: Config, py_env: Optional[PythonEnv] = None) -> None:
    local_modules_paths = py_env.local_modules_paths if py_env is not None else []
    inputs = [input_.path for input_ in config.inputs] + local_modules_paths
    inputs = [Path(input_).absolute() for input_ in inputs]
    _check_paths_do_not_contain_parents(inputs)


def _is_relative_path(path: Path) -> bool:
    return not path.is_absolute() and '..' not in path.as_posix()


def validate_outputs(config: Config) -> None:
    """
    Since we don't know exact state of remote filesystem we can't check all output paths as absolute.
    So we can check path relative to PWD and absolute paths but not relative paths which escape PWD.
    """
    outputs = [Path(output.path) for output in config.outputs]
    relative_outputs = [output for output in outputs if _is_relative_path(output)]
    _check_paths_do_not_contain_parents(relative_outputs)
    absolute_outputs = [output for output in outputs if output.is_absolute()]
    _check_paths_do_not_contain_parents(absolute_outputs)


def validate_paths(config: Config, py_env: Optional[PythonEnv] = None) -> None:
    validate_inputs(config, py_env)
    validate_outputs(config)
