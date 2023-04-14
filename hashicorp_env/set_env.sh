# for the dev server
export VAULT_ADDR='http://127.0.0.1:8200'
# Enterprise license was obtained during investigation of MONGOCRYPT-563.
export VAULT_LICENSE=$(cat ~/.secrets/hashicorp-vault/enterprise-license.txt)
# export VAULT_BIN=~/bin/hashicorp_vault/vault_1.11.8+ent_darwin_arm64/vault
export VAULT_BIN=~/bin/hashicorp_vault/vault_1.13.0+ent_darwin_arm64/vault
# export VAULT_BIN=~/bin/hashicorp_vault/vault_1.13.1+ent_darwin_arm64/vault
# export VAULT_BIN=~/bin/hashicorp_vault/vault-1.13.1-dev-darwin-arm64
echo "Using VAULT_BIN=$VAULT_BIN"
