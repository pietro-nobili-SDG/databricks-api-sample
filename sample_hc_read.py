"""Interact with the vault."""

from typing import Dict, Optional

from hvac.api.secrets_engines.kv_v2 import KvV2
from hvac.exceptions import InvalidPath
from hvac.v1 import Client
from loguru import logger as lg
from requests import Response

from utils import get_hc_client, get_kvv2, jd


def get_client_state():
    """Poll the state of the client."""
    client = get_hc_client()
    lg.debug(f"{client.sys.is_initialized()=}")
    lg.debug(f"{client.sys.is_sealed()=}")
    lg.debug(f"{type(client)=}")


def sample_hc_read():
    """Read a key from the vault.

    Note that the request path will be::

        GET: /{mount_point}/data/{path}.
    """
    client = get_hc_client()
    try:
        read_response: Dict = client.secrets.kv.v2.read_secret_version(path="hello")
    except InvalidPath as e:
        # if the key does not exist fail gracefully
        lg.warning(f"InvalidPath {e}")
        return
    lg.debug(f"{type(read_response)=}")
    lg.debug(f"{jd(read_response['data'])=}")


def sample_hc_write_secret():
    """Write a key to the vault."""
    client = get_hc_client()
    # writing a secret
    create_response: Response = client.secrets.kv.v2.create_or_update_secret(
        path="my-secret-password",
        secret=dict(password="Hashi123"),
    )
    lg.debug(f"{type(create_response)=}")
    lg.debug(f"{create_response=}")


def get_kvv2_type():
    """This is just to have autocomplete on the object."""
    kvv2: KvV2 = get_kvv2()
    lg.debug(type(kvv2))


if __name__ == "__main__":
    get_client_state()
    get_kvv2_type()
    sample_hc_read()
    sample_hc_write_secret()
