package org.example;

import com.mongodb.ClientEncryptionSettings;
import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.client.vault.ClientEncryption;
import com.mongodb.client.vault.ClientEncryptions;
import org.bson.BsonBinary;

import java.security.SecureRandom;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main( String[] args ) {
        byte[] localMasterKey = new byte[96];
        new SecureRandom().nextBytes(localMasterKey);

        Map<String, Map<String, Object>> kmsProviders = new HashMap<String, Map<String, Object>>() {{
            put("local", new HashMap<String, Object>() {{
                put("key", localMasterKey);
            }});
            put("kmip", new HashMap<String, Object>() {{
                put("endpoint", "localhost:5696");
            }});
        }};

        String uri = "mongodb://localhost:27017";
        MongoClientSettings keyVaultClientSettings = MongoClientSettings.builder().applyConnectionString(new ConnectionString(uri)).build();
        ClientEncryptionSettings.Builder ceSettingsBuilder = ClientEncryptionSettings.builder().keyVaultMongoClientSettings(keyVaultClientSettings).kmsProviders(kmsProviders).keyVaultNamespace("db.keyvault");
        ClientEncryptionSettings ceSettings = ceSettingsBuilder.build();
        ClientEncryption ce = ClientEncryptions.create(ceSettings);
        // Create with "local" KMS provider.
        {
            BsonBinary uuid = ce.createDataKey("local");
            System.out.println("created key with 'local' KMS provider with UUID: " + uuid.asUuid());
        }
        // Create with "kmip" KMS provider.
        {
            BsonBinary uuid = ce.createDataKey("kmip");
            System.out.println("created key with 'kmip' KMS provider with UUID: " + uuid.asUuid());
        }
    }
}
