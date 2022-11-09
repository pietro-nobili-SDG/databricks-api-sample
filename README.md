# Databricks API

## Token

* https://docs.databricks.com/administration-guide/access-control/tokens.html
* https://docs.databricks.com/dev-tools/api/latest/authentication.html
* https://learn.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/authentication

1. Click your `username` in the top bar of your Databricks workspace and select `User Settings` from the drop down.
1. Go to the `Access Tokens` tab.
1. Click the `Generate New Token` button.
1. Optionally enter a description (comment) and expiration period.
1. Click `Generate`.
1. Copy the generated token and store in a secure location.

## Secrets

Set them as env var, for the current terminal session.

``` bash
$     export DATABRICKS_TOKEN="secret"
```

Note the space before the command,
to avoid saving it to the bash history.

Better yet: set up a
[HashiCorp vault](https://developer.hashicorp.com/vault)
and use the provided utility functions.

## API

* https://docs.databricks.com/dev-tools/python-api.html

### Clusters (create)

* https://docs.databricks.com/dev-tools/api/latest/clusters.html#request-structure-of-the-cluster-definition
* https://docs.databricks.com/dev-tools/api/latest/clusters.html
* https://github.com/databricks/databricks-cli/blob/main/databricks_cli/clusters/api.py

Create a new Apache Spark cluster. This method acquires new instances from the cloud provider if necessary. This method is asynchronous; the returned cluster_id can be used to poll the cluster state. When this method returns, the cluster is in a PENDING state. The cluster is usable once it enters a RUNNING state.

* **num_workers**, `INT32`: 0.
    A cluster has one Spark driver and num_workers executors for a total of
    num_workers + 1 Spark nodes.
* **cluster_name**, `STR`: Cluster name.
* **spark_version**, `STR`: Runtime version of the cluster.
    For us: `10.4.x-scala2.12`.
* **spark_conf**,
    [`SparkConfPair`](https://docs.databricks.com/dev-tools/api/latest/clusters.html#clustersparkconfpair):
    An object containing a set of optional, user-specified Spark configuration key-value pairs.
    For us: `{ "spark.master": "local[*, 4]", "spark.databricks.cluster.profile": "singleNode" },`.
* **azure_attributes**, `???`: Attributes related to clusters running on Azure.
    For us: `{ "first_on_demand": 1, "availability": "ON_DEMAND_AZURE", "spot_bid_max_price": -1 },`.
* **node_type_id**, `STR`:
    Resources available to each of the Spark nodes in this cluster.
    For us: `Standard_DS3_v2`.
* **custom_tags**,
    [`ClusterTag`](https://docs.databricks.com/dev-tools/api/latest/clusters.html#clusterclustertag):
    A set of tags for cluster resources.
    For us: `{ "ResourceClass": "SingleNode" },`
* **spark_env_vars**,
    [`SparkEnvPair`](https://docs.databricks.com/dev-tools/api/latest/clusters.html#clustersparkenvpair):
    An object containing a set of optional, user-specified environment variable key-value pairs.
    For us: `{ "PYSPARK_PYTHON": "/databricks/python3/bin/python3" },`
* **autotermination_minutes**, `INT32`: 10.
* **enable_elastic_disk**, `BOOL`: `true`? Autoscaling Local Storage.
* **runtime_engine**, `STR`:
    The type of runtime engine to use.
    For us: `STANDARD`.
* **idempotency_token**, `STR`:
    Might be a good idea to avoid repeated requests:
    An optional token that can be used to guarantee the idempotency of cluster creation requests. If the idempotency token is assigned to a cluster that is not in the TERMINATED state, the request does not create a new cluster but instead returns the ID of the existing cluster. Otherwise, a new cluster is created. The idempotency token is cleared when the cluster is terminated.
    If you specify the idempotency token, upon failure you can retry until the request succeeds. Databricks guarantees that exactly one cluster will be launched with that idempotency token.

So hopefully the json payload is:

```json
{
    "num_workers": 0,
    "cluster_name": "cluster_name",
    "spark_version": "10.4.x-scala2.12",
    "spark_conf": {
        "spark.master": "local[*, 4]",
        "spark.databricks.cluster.profile": "singleNode"
    },
    "azure_attributes": {
        "first_on_demand": 1,
        "availability": "ON_DEMAND_AZURE",
        "spot_bid_max_price": -1
    },
    "node_type_id": "Standard_DS3_v2",
    "custom_tags": {
        "ResourceClass": "SingleNode"
    },
    "spark_env_vars": {
        "PYSPARK_PYTHON": "/databricks/python3/bin/python3"
    },
    "autotermination_minutes": 10,
    "enable_elastic_disk": true,
    "runtime_engine": "STANDARD",
}
```

```python
api_client = get_databricks_client()
cluster_api = ClusterApi(api_client)
json_conf = ...
cluster_api.create_cluster(json_conf)
```

### Jobs
