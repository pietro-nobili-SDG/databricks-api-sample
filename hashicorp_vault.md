# Use HashiCorp vault to store secrets

## Deploy and start the vault

* https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-deploy

### Set up config file

Save in `config.hcl`:

```bash
storage "raft" {
  path    = ".vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
```

TODO: should learn how to use TLS.

### Start the server

```bash
vault server -config=config.hcl
```

### Initialize the vault

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
```

```bash
vault operator init
```

or for local use

```bash
vault operator init -key-shares=1 -key-threshold=1
```

which will produce

```
Unseal Key 1: mega_secret_key

Initial Root Token: s.mega_secret_token

Vault initialized with 1 key shares and a key threshold of 1. Please securely
distribute the key shares printed above. When the Vault is re-sealed, restarted,
or stopped, you must supply at least 1 of these keys to unseal it before it can
start servicing requests.

Vault does not store the generated root key. Without at least 1 keys to
reconstruct the root key, Vault will remain permanently sealed!  It is possible

to generate new unseal keys, provided you have a quorum of existing unseal keys
shares. See "vault operator rekey" for more information. 
```

### Unseal the vault

```bash
vault operator unseal
```

and paste the unseal keys one by one.
This can be done bu multiple operators from multiple computers,
and the unseal keys should not be stored together.

Now the vault is unsealed for every user.

A root user can seal the vault

```bash
vault operator seal
```

### Login to the vault

```bash
vault login
```

and paste the vault token.

### Add a secret engine

* https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-secrets-engines

```
vault secrets enable -path=secret/ kv
```

You are now ready to store and read secrets.

## Token authentication

* https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-authentication

### Create a token

When running `vault operator init` you get a root token.

This can be used to do many things,
including creating new tokens.

```bash
vault token create
```

This token is a child of the root token, and by default, it inherits the policies from its parent.

TODO: learn to create policies and do not let this token have root access.

### GitHub authentication

GitHub authentication enables a user to authenticate with Vault by providing their GitHub credentials and receive a Vault token.

## Store and read secrets

### Python [HVAC](https://github.com/hvac/hvac)

For mystical reasons the python interface adds `data` as prefix?
Which is documented in `read_secret_version` and `create_or_update_secret`:
`GET: /{mount_point}/data/{path}. Produces: 200 application/json`
but still. Why.

```bash
vault kv put -mount=secret data/hello foo=world
```