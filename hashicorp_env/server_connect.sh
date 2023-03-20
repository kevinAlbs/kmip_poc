CERT_PATH=/Users/kevin.albertson/.secrets/hashicorp-vault/kmip_certs
# Connect directly to the KMIP server.
openssl s_client -connect localhost:5696 -cert $CERT_PATH/cert.pem -key $CERT_PATH/key.pem -CAfile $CERT_PATH/ca.pem