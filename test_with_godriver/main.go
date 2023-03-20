package main

// An example of creating a data key with KMIP.
// Run with: go run -tags cse .
//
// Set the environment variables KMIP_TLS_CERTIFICATE_KEY_FILE and KMIP_TLS_CA_FILE to configure KMIP TLS.
//
// Set the environment variable KMS_PROVIDERS_PATH to the path of a JSON file with KMS credentials.
// KMS_PROVIDERS_PATH defaults to ./kms_providers.json.
//
// Set the environment variable MONGODB_URI to set a custom URI. MONGODB_URI defaults to
// mongodb://localhost:27017.

import (
	"context"
	"crypto/tls"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/bsontype"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/x/bsonx/bsoncore"
)

// readFile reads a file into a byte slice.
func readFile(path string) []byte {
	file, err := os.Open(path)
	defer file.Close()

	if err != nil {
		log.Panicf("error in Open: %v", err)
	}
	contents, err := ioutil.ReadAll(file)
	if err != nil {
		log.Panicf("error in ReadAll: %v", err)
	}

	return contents
}

// getKMSProvidersFromFile reads a JSON file for use as the KmsProviders option.
func getKMSProvidersFromFile(path string) map[string]map[string]interface{} {
	var kmsProviders map[string]map[string]interface{}
	contents := readFile(path)
	err := bson.UnmarshalExtJSON(contents, false, &kmsProviders)
	if err != nil {
		log.Panicf("error in UnmarshalExtJSON: %v", err)
	}

	return kmsProviders
}

// getKMIPTLSConfig returns TLS config for KMIP if certificates are passed.
// Certificate file paths can be passed through the environment variables:
// KMIP_TLS_CA_FILE and KMIP_TLS_CERTIFICATE_KEY_FILE
func getKMIPTLSConfig() *map[string]*tls.Config {
	// Configure TLS config if certificates for KMIP were passed.
	tlsCAFileKMIP := os.Getenv("KMIP_TLS_CA_FILE")
	tlsClientCertificateKeyFileKMIP := os.Getenv("KMIP_TLS_CERTIFICATE_KEY_FILE")
	tlsConfig := make(map[string]*tls.Config)
	if tlsCAFileKMIP != "" && tlsClientCertificateKeyFileKMIP != "" {
		tlsOpts := map[string]interface{}{
			"tlsCertificateKeyFile": tlsClientCertificateKeyFileKMIP,
			"tlsCAFile":             tlsCAFileKMIP,
		}
		kmipConfig, err := options.BuildTLSConfig(tlsOpts)
		if err != nil {
			log.Panicf("failed to build TLS config: %v", err)
		}
		tlsConfig["kmip"] = kmipConfig
		return &tlsConfig
	}
	return nil
}

func main() {
	var uri string
	if uri = os.Getenv("MONGODB_URI"); uri == "" {
		uri = "mongodb://localhost:27017"
	}

	var kmsProvidersPath string
	if kmsProvidersPath = os.Getenv("KMS_PROVIDERS_PATH"); kmsProvidersPath == "" {
		kmsProvidersPath = "./kms_providers.json"
	}

	keyvaultClient, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(uri))
	if err != nil {
		log.Panicf("Connect error: %v\n", err)
	}
	defer keyvaultClient.Disconnect(context.TODO())

	kmsProviders := getKMSProvidersFromFile(kmsProvidersPath)

	// A ClientEncryption struct provides admin helpers with three functions:
	// 1. create a data key
	// 2. explicit encrypt
	// 3. explicit decrypt
	ceopts := options.ClientEncryption().
		SetKmsProviders(kmsProviders).
		SetKeyVaultNamespace("keyvault.datakeys")

	if tlsConfig := getKMIPTLSConfig(); tlsConfig != nil {
		ceopts.SetTLSConfig(*tlsConfig)
	}

	ce, err := mongo.NewClientEncryption(keyvaultClient, ceopts)
	if err != nil {
		log.Panicf("NewClientEncryption error: %v\n", err)
	}

	fmt.Printf("CreateDataKey... begin\n")
	keyid, err := ce.CreateDataKey(context.TODO(), "kmip", options.DataKey())
	if err != nil {
		log.Panicf("CreateDataKey error: %v\n", err)
	}
	fmt.Printf("Created key with a UUID: %v\n", hex.EncodeToString(keyid.Data))
	fmt.Printf("CreateDataKey... end\n")

	fmt.Printf("Encrypt... begin\n")
	plaintext := bson.RawValue{Type: bsontype.String, Value: bsoncore.AppendString(nil, "test")}
	eOpts := options.Encrypt().SetAlgorithm("AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic").SetKeyID(keyid)
	ciphertext, err := ce.Encrypt(context.TODO(), plaintext, eOpts)
	if err != nil {
		log.Panicf("Encrypt error: %v\n", err)
	}
	fmt.Printf("Explicitly encrypted to ciphertext: %x\n", ciphertext)
	fmt.Printf("Encrypt... end\n")

	fmt.Printf("Decrypt... begin\n")
	plaintext, err = ce.Decrypt(context.TODO(), ciphertext)
	if err != nil {
		log.Panicf("Decrypt error: %v\n", err)
	}
	fmt.Printf("Explicitly decrypted to plaintext: %v\n", plaintext)
	fmt.Printf("Decrypt... end\n")

}

/* Sample output
CreateDataKey... begin
Created key with a UUID: 9810165bb6b24c0b852634929928d244
CreateDataKey... end
Encrypt... begin
Explicitly encrypted to ciphertext: {6 019810165bb6b24c0b852634929928d2440292cac8eece447c5139e070c985a3544ea39b467db29e05350440238092a6a988c4f855f4b617bf66042e45aa4262697b5b8eb777fdafcfc7b3935cbee691599d}
Encrypt... end
Decrypt... begin
Explicitly decrypted to plaintext: "test"
Decrypt... end
*/
