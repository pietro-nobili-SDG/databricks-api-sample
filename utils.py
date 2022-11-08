"""Utilities to interact with the API."""
import os

from loguru import logger as lg

HOST = "https://adb-8552426296089162.2.azuredatabricks.net/"


def get_env(
    env_var_name_token="DATABRICKS_TOKEN",
):
    """Get the requested environment variable.

    With some pretty log errors.
    """
    token = os.getenv(env_var_name_token)
    if token is None:
        lg.error(
            f"Missing {env_var_name_token} environment variable. "
            "Please add it using"
            f' export {env_var_name_token}="secret".'
            " Remember to type a space before the command,"
            " to avoid saving it to your bash history."
        )
        raise KeyError(f"Missing {env_var_name_token} environment variable.")
    return token
