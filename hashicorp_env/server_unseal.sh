. ./set_env.sh

vault operator unseal $(cat ~/.hashicorp_vault/unseal_key1.txt)
vault operator unseal $(cat ~/.hashicorp_vault/unseal_key2.txt)
vault operator unseal $(cat ~/.hashicorp_vault/unseal_key3.txt)