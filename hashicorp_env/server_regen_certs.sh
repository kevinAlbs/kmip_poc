. ./set_env.sh

CERT_PATH=/Users/kevin.albertson/.secrets/hashicorp-vault/kmip_certs

$VAULT_BIN write -format=json \
    kmip/scope/finance/role/accounting/credential/generate \
    format=pem > $CERT_PATH/credential.json


jq -r .data.certificate < $CERT_PATH/credential.json > $CERT_PATH/cert.pem
jq -r .data.private_key < $CERT_PATH/credential.json > $CERT_PATH/key.pem

cat $CERT_PATH/cert.pem $CERT_PATH/key.pem > $CERT_PATH/key_with_cert.pem