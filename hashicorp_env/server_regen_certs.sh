. ./set_env.sh

CERT_PATH=/Users/kevin.albertson/.hashicorp_vault/kmip_certs

vault write -format=json \
    kmip/scope/finance/role/accounting/credential/generate \
    format=pem > $CERT_PATH/credential.json


jq -r .data.certificate < $CERT_PATH/credential.json > $CERT_PATH/cert.pem
jq -r .data.private_key < $CERT_PATH/credential.json > $CERT_PATH/key.pem
