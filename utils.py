"""Utilities to interact with the API."""
from databricks_cli.sdk.api_client import ApiClient
import json
import os
from typing import Any, Dict, Optional

import hvac
from hvac.api.secrets_engines.kv_v2 import KvV2
from hvac.exceptions import InvalidPath
from hvac.v1 import Client
from loguru import logger as lg

# databricks host
HOST = "https://adb-8552426296089162.2.azuredatabricks.net/"

# name of the environment variable
ENV_DATABRICKS_TOKEN = "DATABRICKS_TOKEN"

# path in the vault
HC_DATABRICKS_PATH = "databricks"
# key in the vault, at that path
HC_DATABRICKS_TOKEN = "TOKEN"


##################################################
#    Get secret from environment
##################################################


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


##################################################
#    Databricks API utils
##################################################


def get_databricks_client() -> ApiClient:
    """Get the ApiClient with default host/secret."""
    api_client = ApiClient(
        host=HOST,
        token=get_secret_from_hc(HC_DATABRICKS_PATH, HC_DATABRICKS_TOKEN),
    )
    return api_client


##################################################
#    Misc utils
##################################################


def jd(json_obj: object, indent=4, **kwargs) -> str:
    """A thin wrapper around json.dumps with default 4 indent."""
    return json.dumps(json_obj, indent=indent, **kwargs)


##################################################
#    HashiCorp utils
##################################################


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


def get_secret_from_hc(path: str, key: Optional[str] = None) -> Dict[str, str]:
    """Get the requested secret from the active vault."""
    kvv2 = get_kvv2()
    # get the path
    try:
        read_response: Dict = kvv2.read_secret_version(path=path)
    except InvalidPath as e:
        lg.error(f"Missing {path=} in the vault.")
        raise KeyError(f"Missing {path=} in the vault.")
    # grab the data from the response dict
    data = read_response["data"]
    # if we have no key return the whole path
    if key is None:
        return data
    # search for the key and return that
    if key not in data:
        lg.error(f"Missing {key=} in the read data.")
        raise KeyError(f"Missing {key=} in the read data.")
    return data[key]
