"""Sample interface with databricks API.

https://docs.databricks.com/dev-tools/python-api.html
"""

import json
from typing import Dict

from databricks_cli.clusters.api import ClusterApi
from loguru import logger as lg
from requests import Response

from utils import get_databricks_client, jd

CREATE_TEMPLATE = """{{
    "num_workers": 0,
    "cluster_name": "{cluster_name}",
    "spark_version": "10.4.x-scala2.12",
    "spark_conf": {{
        "spark.master": "local[*, 4]",
        "spark.databricks.cluster.profile": "singleNode"
    }},
    "azure_attributes": {{
        "first_on_demand": 1,
        "availability": "ON_DEMAND_AZURE",
        "spot_bid_max_price": -1
    }},
    "node_type_id": "Standard_DS3_v2",
    "custom_tags": {{
        "ResourceClass": "SingleNode"
    }},
    "spark_env_vars": {{
        "PYSPARK_PYTHON": "/databricks/python3/bin/python3"
    }},
    "autotermination_minutes": {autotermination_minutes},
    "enable_elastic_disk": true,
    "runtime_engine": "STANDARD"
}}
"""


def sample_create_cluster():
    """Sample use of the create_cluster func."""
    # get the api handler
    api_client = get_databricks_client()
    cluster_api = ClusterApi(api_client)

    # build the string and get a dict from it
    json_conf_str = CREATE_TEMPLATE.format(
        cluster_name="test_databricks_api_01",
        autotermination_minutes=10,
    )
    lg.info("Will create cluster with conf string:\n{}", json_conf_str)
    json_conf = json.loads(json_conf_str)

    # add a debug idempotency token so we can spam this request
    json_conf.update({"idempotency_token": "testing_testing_123"})
    lg.info("Will create cluster with conf:\n{}", json_conf)

    # create the cluster
    create_response: Dict = cluster_api.create_cluster(json_conf)

    # get the id
    lg.debug(f"{type(create_response)=}")
    lg.debug(f"{jd(create_response)=}")
    lg.debug(f"{create_response['cluster_id']=}")


if __name__ == "__main__":
    sample_create_cluster()
