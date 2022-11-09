# pasted from
# https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-deploy#configuring-vault
# uses unsecure tsl_disable mode

storage "raft" {
  path    = "/home/pmn/.hc-vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
