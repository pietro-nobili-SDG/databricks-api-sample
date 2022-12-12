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

    cluster_name = "ds_dev_fcst_inbound_01"
    # this actually returns a list of cluster info
    # cluster_ids = cluster_api.get_cluster_ids_by_name(cluster_name)
    clusters = cluster_api.get_cluster_ids_by_name(cluster_name)
    for cluster in clusters:
        lg.info("{}: {}", cluster_name, cluster["cluster_id"])


def get_cluster_id_by_name(
    cluster_name: str,
) -> str:
    """A wrapper for cluster_api.get_cluster_ids_by_name.

    We assume there is a single cluster by that name.

    Raises:
        KeyError: If there are no cluster by that name.

    Returns:
        str: The cluster id.
    """
    api_client = get_databricks_client()
    cluster_api = ClusterApi(api_client)

    # this actually returns a list of cluster info
    clusters = cluster_api.get_cluster_ids_by_name(cluster_name)
    # for cluster in clusters:
    #     lg.info("{}: {}", cluster_name, cluster["cluster_id"])

    if len(clusters) == 0:
        raise KeyError(f"There are {len(clusters)} cluster named {cluster_name}.")

    if len(clusters) != 1:
        lg.warning("There are {} cluster named {}.", len(clusters), cluster_name)

    # we still return the first
    cluster = clusters[0]

    return cluster["cluster_id"]


if __name__ == "__main__":
    sample_list_cluster()
