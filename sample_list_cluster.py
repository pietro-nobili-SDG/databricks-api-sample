"""Sample interface with databricks API.

https://docs.databricks.com/dev-tools/python-api.html
"""

import json

from databricks_cli.clusters.api import ClusterApi
from loguru import logger as lg

from utils import get_databricks_client


def sample_list_cluster():
    """Sample use of the list_cluster function.

    https://docs.databricks.com/dev-tools/python-api.html
    """

    api_client = get_databricks_client()

    cluster_api = ClusterApi(api_client)
    clusters_list = cluster_api.list_clusters()

    lg.info("Cluster name, cluster ID")
    for cluster in clusters_list["clusters"]:
        lg.info(f"{cluster['cluster_name']}, {cluster['cluster_id']}")

    cluster = clusters_list["clusters"][0]
    lg.info(json.dumps(cluster, indent=4))


if __name__ == "__main__":
    sample_list_cluster()
