"""Sample interface with databricks API.

https://docs.databricks.com/dev-tools/python-api.html
"""

import json

from databricks_cli.clusters.api import ClusterApi
from databricks_cli.sdk.api_client import ApiClient
from loguru import logger as lg

from utils import ENV_DATABRICKS_TOKEN, HOST, get_env


def sample_list_cluster():
    """Sample use of the list_cluster function.

    https://docs.databricks.com/dev-tools/python-api.html
    """

    api_client = ApiClient(
        host=HOST,
        token=get_env(ENV_DATABRICKS_TOKEN),
    )

    cluster_api = ClusterApi(api_client)
    clusters_list = cluster_api.list_clusters()

    lg.info("Cluster name, cluster ID")
    for cluster in clusters_list["clusters"]:
        lg.info(f"{cluster['cluster_name']}, {cluster['cluster_id']}")

    lg.info(json.dumps(cluster, indent=4))


if __name__ == "__main__":
    sample_list_cluster()
