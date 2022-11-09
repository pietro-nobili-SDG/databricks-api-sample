"""Utilities to interact with the API."""
import json
import os
from typing import Any, Dict, Optional

import hvac
from hvac.api.secrets_engines.kv_v2 import KvV2
from hvac.v1 import Client
from loguru import logger as lg

HOST = "https://adb-8552426296089162.2.azuredatabricks.net/"
ENV_DATABRICKS_TOKEN = "DATABRICKS_TOKEN"


def get_env(env_var_name):
    """Get the requested environment variable.

    With some pretty log errors.
    """
    token = os.getenv(env_var_name)
    if token is None:
        lg.error(
            f"Missing {env_var_name} environment variable. "
            "Please add it using"
            f' export {env_var_name}="secret".'
            " Remember to type a space before the command,"
            " to avoid saving it to your bash history."
        )
        raise KeyError(f"Missing {env_var_name} environment variable.")
    return token


def jd(obj: Any) -> str:
    """Json dumps an object."""
    return json.dumps(obj)


def get_hc_client() -> Client:
    """Get the local HashiCorp client."""
    client = hvac.Client(url="http://localhost:8200")
    return client


def get_kvv2(client: Optional[Client] = None) -> KvV2:
    """Get the KvV2 object."""
    if client is None:
        client = get_hc_client()
    kvv2: KvV2 = client.secrets.kv.v2
    return kvv2
