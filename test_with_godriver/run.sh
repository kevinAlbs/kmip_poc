# If needed: go clean -cache -testcache
CERT_PATH=/Users/kevin.albertson/.secrets/hashicorp-vault/kmip_certs
export KMIP_TLS_CERTIFICATE_KEY_FILE=$CERT_PATH/key_with_cert.pem
export KMIP_TLS_CA_FILE=$CERT_PATH/ca.pem
export PKG_CONFIG_PATH=~/code/c-bootstrap/install/libmongocrypt-1.7.3/lib/pkgconfig
export DYLD_LIBRARY_PATH=~/code/c-bootstrap/install/libmongocrypt-1.7.3/lib/
pushd test_with_godriver
go run -tags cse .
popd
