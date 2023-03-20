. ./set_env.sh

$VAULT_BIN operator unseal $(cat ~/.secrets/hashicorp-vault/unseal_key1.txt)
$VAULT_BIN operator unseal $(cat ~/.secrets/hashicorp-vault/unseal_key2.txt)
$VAULT_BIN operator unseal $(cat ~/.secrets/hashicorp-vault/unseal_key3.txt)