# Prepare certificates for Java driver to authenticate to Hashicorp Vault server over TLS.
# Copied and modified from: https://github.com/mongodb/mongo-java-driver/blob/master/.evergreen/run-csfle-tests-with-mongocryptd.sh
# After running, add these Java system properties to IntelliJ:
# -Djavax.net.ssl.enabled=true
# -Djavax.net.ssl.keyStoreType=pkcs12
# -Djavax.net.ssl.keyStore=/Users/kevin.albertson/code/kmip_poc/client.pkc
# -Djavax.net.ssl.keyStorePassword=bithere
# -Djavax.net.ssl.trustStoreType=jks
# -Djavax.net.ssl.trustStore=/Users/kevin.albertson/code/kmip_poc/mongo-truststore
# -Djavax.net.ssl.trustStorePassword=changeit
rm client.pkc
rm mongo-truststore
DRIVERS_TOOLS=/Users/kevin.albertson/code/drivers-evergreen-tools
KMIP_TLS_CERTIFICATE_KEY_FILE=${DRIVERS_TOOLS}/.evergreen/x509gen/client.pem
KMIP_TLS_CA_FILE=${DRIVERS_TOOLS}/.evergreen/x509gen/ca.pem
openssl pkcs12 -CAfile $KMIP_TLS_CA_FILE -export -in $KMIP_TLS_CERTIFICATE_KEY_FILE -out client.pkc -password pass:bithere
keytool -importcert -trustcacerts -file $KMIP_TLS_CA_FILE -keystore mongo-truststore -storepass changeit -storetype JKS -noprompt
