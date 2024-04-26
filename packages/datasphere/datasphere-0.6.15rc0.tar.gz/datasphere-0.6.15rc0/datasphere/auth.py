from datetime import datetime, timedelta
import logging
import os
import requests
import subprocess
from typing import List, Optional, Tuple

import grpc

from datasphere.api import env, ServerEnv, iam_endpoint
from datasphere.version import version
from yandex.cloud.iam.v1.iam_token_service_pb2 import CreateIamTokenRequest
from yandex.cloud.iam.v1.iam_token_service_pb2_grpc import IamTokenServiceStub

logger = logging.getLogger(__name__)

oauth_token_env_var_1 = 'YC_TOKEN'  # As in `yc`
oauth_token_env_var_2 = 'YC_OAUTH_TOKEN'  # More consistent with IAM token env var
# Announced in https://bb.yandexcloud.net/projects/CLOUD/repos/cloud-go/browse/cli/CHANGELOG.md
iam_token_env_var = 'YC_IAM_TOKEN'


# We support all auth subjects:
# 1) Usual users
# 2) Federate users
# 3) Service accounts
#
# For 1), user can provide OAuth token, so we generate IAM token with it.
# If OAuth token was not provided, we use `yc` utility as a fallback.
#
# For 2), we delegate auth to `yc` utility, which can handle SSA.
#
# For 3), we either in environment with YC metadata server linked with this SA (Compute Instance, Managed Airflow pod),
# otherwise we delegate auth to `yc` utility.
#
# In case of delegating auth to `yc`, we consider that it configured properly to the corresponding auth subject.
def create_iam_token(oauth_token: Optional[str], yc_profile: Optional[str] = None) -> str:
    if oauth_token:
        return create_iam_token_by_oauth_token(oauth_token)

    return create_iam_token_with_compute_metadata() or create_iam_token_with_yc(yc_profile)


def create_iam_token_by_oauth_token(oauth_token: str) -> str:
    logger.debug('creating iam token using oauth token ...')
    stub = IamTokenServiceStub(grpc.secure_channel(iam_endpoint, grpc.ssl_channel_credentials()))
    req = CreateIamTokenRequest(yandex_passport_oauth_token=oauth_token)
    resp = stub.Create(req)
    return resp.iam_token


metadata_host = os.getenv('YC_METADATA_ADDR', '169.254.169.254')
metadata_server_is_up: Optional[bool] = None  # before first connection check


# This logic duplicates original one from `yandexcloud`, but since we can't use `yandexcloud` because of `protobuf`
# dependencies issues, we moved it here. This logic, including environment variable names, is unlikely to change.
# See https://yandex.cloud/ru/docs/compute/operations/vm-connect/auth-inside-vm#api_3
def create_iam_token_with_compute_metadata() -> Optional[str]:
    global metadata_server_is_up
    if metadata_server_is_up is False:
        return None

    try:
        resp = requests.get(
            f'http://{metadata_host}/computeMetadata/v1/instance/service-accounts/default/token',
            headers={'Metadata-Flavor': 'Google'},
            timeout=1,
        )
    except requests.exceptions.ConnectTimeout:
        if metadata_server_is_up:
            logger.error('metadata server was up but now is down')
        metadata_server_is_up = False
        return None
    except Exception as e:
        logger.error('unexpected exception during request to metadata server')
        logger.exception(e)
        metadata_server_is_up = False
        return None

    if metadata_server_is_up is None:
        logger.debug('metadata server found on host %s', metadata_host)
        metadata_server_is_up = True

    logger.debug('iam token is retrieved from metadata server')
    return resp.json()['access_token']


def create_iam_token_with_yc(yc_profile: Optional[str] = None) -> str:
    env_token: Optional[str] = os.environ.get(iam_token_env_var)
    if env_token:
        logger.warning('iam token from env var is not refreshable, so it may expire over time')
        return env_token
    logger.debug('oauth token is not provided, creating iam token through `yc` ...')
    try:
        # TODO: capture stderr, process return code
        cmd = ['yc', 'iam', 'create-token', '--no-user-output']
        if yc_profile:
            cmd += ['--profile', yc_profile]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    except FileNotFoundError:
        raise RuntimeError('You have not provided OAuth token. You have to install Yandex Cloud CLI '
                           '(https://cloud.yandex.com/docs/cli/) to authenticate automatically.')

    # There may be another output before the token, for example, info about opening the browser.
    # TODO: not sure if token will be last line (update suggestion appears regardless of --no-user-output flag
    return process.stdout.strip().split('\n')[-1]


iam_token_refresh_period = timedelta(hours=1)  # 12h is maximum for IAM token
iam_token_refreshed_at: Optional[datetime] = None
current_iam_token: Optional[str] = None


def get_md(oauth_token: Optional[str], yc_profile: Optional[str] = None) -> List[Tuple[str, str]]:
    metadata = [("x-client-version", f"datasphere={version}")]

    if env == ServerEnv.DEV:
        return metadata

    global current_iam_token
    global iam_token_refreshed_at
    now = datetime.now()

    iam_token_expired = iam_token_refreshed_at is None or now - iam_token_refreshed_at > iam_token_refresh_period
    if iam_token_expired:
        current_iam_token = create_iam_token(oauth_token, yc_profile)
        iam_token_refreshed_at = now

    assert current_iam_token

    metadata.append(('authorization', f'Bearer {current_iam_token}'))
    return metadata
