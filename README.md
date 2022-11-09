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

## API

* https://docs.databricks.com/dev-tools/python-api.html

### Clusters

* https://docs.databricks.com/dev-tools/api/latest/clusters.html
* https://github.com/databricks/databricks-cli/blob/main/databricks_cli/clusters/api.py