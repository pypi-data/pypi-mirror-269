import base64
import hashlib
import io
import logging
from unittest.mock import Mock
import requests
from typing import BinaryIO

from datasphere.api import jobs_pb2 as jobs
from datasphere.config import VariablePath

from datasphere.files import prepare_local_modules, upload_files, download_files
from datasphere.pyenv import PythonEnv


def test_prepare_local_modules(tmp_path, mocker):
    py_env = PythonEnv(
        version='',
        local_modules_paths=['main.py', 'lib/'],
        requirements=[],
    )

    # mock archive with file with module name as content
    def zip_path(module: str, ar: BinaryIO):
        with open(ar.name, 'w') as ar_w:
            ar_w.write(module)
            ar_w.seek(0)

    mocker.patch('datasphere.files.zip_path', zip_path)

    paths = prepare_local_modules(py_env, str(tmp_path))

    for path, expected_var, expected_hash in (
            (paths[0], '_LOCAL_MODULE_0', hashlib.sha256(b'main.py').hexdigest()),
            (paths[1], '_LOCAL_MODULE_1', hashlib.sha256(b'lib/').hexdigest())
    ):
        assert path.path.startswith(str(tmp_path))
        assert path.var == expected_var
        f = path.get_file()
        assert f.desc.path == path.path
        assert f.desc.var == expected_var
        assert f.sha256 == expected_hash


def test_upload_files(tmp_path, mocker, caplog):
    file_1 = tmp_path / '1.txt'
    file_2 = tmp_path / '2.txt'
    dir_3 = tmp_path / '3'
    zip_dir_3 = dir_3.with_suffix('.zip')

    file_1.write_text('qwerty')
    file_2.write_text('foo')
    zip_dir_3.write_text('zip dir content')

    files = [
        jobs.StorageFile(
            file=jobs.File(
                desc=jobs.FileDesc(path=str(file_1.absolute())),
                sha256='file1_sha256',
            ),
            url='https://storage.net/my-bucket/my-key-1',
        ),
        jobs.StorageFile(
            file=jobs.File(
                desc=jobs.FileDesc(path=str(file_2.absolute())),
                sha256='file2_sha256',
            ),
            url='https://storage.net/my-bucket/my-key-2',
        ),
        jobs.StorageFile(
            file=jobs.File(
                desc=jobs.FileDesc(path=str(zip_dir_3.absolute())),
                sha256='dir3_sha256',
                compression_type=jobs.FileCompressionType.ZIP
            ),
            url='https://storage.net/my-bucket/my-key-3',
        ),
    ]

    sha256_to_display_path = {'file2_sha256': 'pretty_path.txt'}

    contents = []

    # Let upload content be file content along with url
    def put(url: str, data: BinaryIO):
        contents.append(url.encode('utf8') + b' ' + data.read())
        return Mock(status_code=200)

    mocker.patch('requests.put', put)

    caplog.set_level(logging.DEBUG)

    upload_files(files, [VariablePath(path=str(dir_3), _archive_path=str(zip_dir_3))], sha256_to_display_path)

    assert contents == [
        b'https://storage.net/my-bucket/my-key-1 qwerty',
        b'https://storage.net/my-bucket/my-key-2 foo',
        b'https://storage.net/my-bucket/my-key-3 zip dir content',
    ]
    assert caplog.record_tuples == [
        ('datasphere.files', 20, 'uploading 3 files (0.0B) ...'),
        ('datasphere.files', 10, f'uploading file `{tmp_path}/1.txt` (0.0B) ...'),
        ('datasphere.files', 10, 'uploading file `pretty_path.txt` (0.0B) ...'),
        ('datasphere.files', 10, f'uploading file `{tmp_path}/3.zip` (0.0B) ...'),
        ('datasphere.files', 20, 'files are uploaded'),
    ]


def test_download_files(tmp_path, mocker, caplog):
    file_1 = tmp_path / '1.txt'
    file_2 = tmp_path / 'dir' / 'subdir' / '2.txt'  # Sub dirs will be created automatically.
    dir_3 = tmp_path / 'zipped'

    # File which we download will contain url as first line, then offset of chunk.
    def get(url: str) -> requests.Response:
        resp = Mock(status_code=200)

        bytes_ = b'unknown'
        if url.endswith("my-key-1"):
            bytes_ = io.BytesIO(url.encode() + b" file 1 content")
        elif url.endswith("my-key-2"):
            bytes_ = io.BytesIO(url.encode() + b" file 2 content")
        elif url.endswith("my-key-3"):
            bytes_ = io.BytesIO(base64.decodebytes(ZIPPED_DIR_ARCHIVE_BASE64))

        def iter_bytes(chunk_size: int) -> bytes:
            while len(chunk := bytes_.read(chunk_size)) > 0:
                yield chunk

        resp.iter_content = iter_bytes
        return resp

    mocker.patch('requests.get', get)

    files = [
        jobs.StorageFile(
            file=jobs.File(
                desc=jobs.FileDesc(path=str(file_1.absolute())),
                sha256='',  # not important
            ),
            url='https://storage.net/my-bucket/my-key-1',
        ),
        jobs.StorageFile(
            file=jobs.File(
                desc=jobs.FileDesc(path=str(file_2.absolute())),
                sha256='',  # not important
            ),
            url='https://storage.net/my-bucket/my-key-2',
        ),
        jobs.StorageFile(
            file=jobs.File(
                desc=jobs.FileDesc(path=str(dir_3.absolute())),
                sha256='',  # not important
                compression_type=jobs.FileCompressionType.ZIP,
            ),
            url='https://storage.net/my-bucket/my-key-3',
        ),
    ]

    caplog.set_level(logging.DEBUG)

    download_files(files)

    assert file_1.read_text() == 'https://storage.net/my-bucket/my-key-1 file 1 content'
    assert file_2.read_text() == 'https://storage.net/my-bucket/my-key-2 file 2 content'
    assert dir_3.exists()
    assert dir_3.is_dir()
    assert (dir_3 / "file3.txt").exists()
    assert (dir_3 / 'file3.txt').read_text().strip() == 'file 3 content'

    assert caplog.record_tuples == [
        ('datasphere.files', 20, 'downloading 3 files (0.0B) ...'),
        ('datasphere.files', 10, f'downloading file `{tmp_path}/1.txt` (0.0B) ...'),
        ('datasphere.files', 10, f'downloading file `{tmp_path}/dir/subdir/2.txt` (0.0B) ...'),
        ('datasphere.files', 10, f'downloading file `{tmp_path}/zipped` (0.0B) ...'),
        ('datasphere.files', 10,
         f'File `{tmp_path}/zipped.download` is compressed with ZIP. Rename to `{tmp_path}/zipped.zip`'),
        ('datasphere.files', 10, f'Uncompressing ZIP file `{tmp_path}/zipped.zip`'),
        ('datasphere.files', 10, f'ZIP file `{tmp_path}/zipped.zip` uncompressed'),
        ('datasphere.files', 10, f'Original ZIP file `{tmp_path}/zipped.zip` removed'),
        ('datasphere.files', 20, 'files are downloaded'),
    ]


ZIPPED_DIR_ARCHIVE_BASE64 = b'UEsDBAoAAAAAACmFhVgAAAAAAAAAAAAAAAAHABwAemlwcGVkL1VUCQADfv8PZpf/D2Z1eAsAAQT+Iu89BL4wYiNQSwMECgACAAAAKYWFWOupjM4PAAAADwAAABAAHAB6aXBwZWQvZmlsZTMudHh0VVQJAAN+/w9mf/8PZnV4CwABBP4i7z0EvjBiI2ZpbGUgMyBjb250ZW50ClBLAQIeAwoAAAAAACmFhVgAAAAAAAAAAAAAAAAHABgAAAAAAAAAEADtQQAAAAB6aXBwZWQvVVQFAAN+/w9mdXgLAAEE/iLvPQS+MGIjUEsBAh4DCgACAAAAKYWFWOupjM4PAAAADwAAABAAGAAAAAAAAQAAAKSBQQAAAHppcHBlZC9maWxlMy50eHRVVAUAA37/D2Z1eAsAAQT+Iu89BL4wYiNQSwUGAAAAAAIAAgCjAAAAmgAAAAAA'
