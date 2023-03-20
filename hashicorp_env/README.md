# How to set up a test environment for Hashicorp Vault with KMIP

Download the Enterprise Binary of Vault following the "Prerequisites" here: https://developer.hashicorp.com/nomad/tutorials/enterprise/hashicorp-enterprise-license

Follow the Getting Started Deploy instructions to start a vault server.
https://learn.hashicorp.com/tutorials/vault/getting-started-deploy?in=vault/getting-started

Verify enterprise license is loaded:
```
(.venv) kevin.albertson@M-PGWJ0XYHJF hashicorp_env % $VAULT_BIN  read sys/license/status
WARNING! The following warnings were returned from Vault:

  * time left on license is 658h2m26s

Key                   Value
---                   -----
autoloaded            map[expiration_time:2023-04-17T00:00:00Z features:[DR Replication Namespaces KMIP Lease Count Quotas Key Management Secrets Engine Automated Snapshots Key Management Transparent Data Encryption] license_id:0981121a-2047-a230-67d2-678a12566aee performance_standby_count:0 start_time:2023-03-17T00:00:00Z termination_time:2023-04-17T00:00:00Z]
autoloading_used      true
persisted_autoload    map[expiration_time:2023-04-17T00:00:00Z features:[DR Replication Namespaces KMIP Lease Count Quotas Key Management Secrets Engine Automated Snapshots Key Management Transparent Data Encryption] license_id:0981121a-2047-a230-67d2-678a12566aee performance_standby_count:0 start_time:2023-03-17T00:00:00Z termination_time:2023-04-17T00:00:00Z]
```

Verify server works with the KV secrets engine:
```
(.venv) kevin.albertson@M-PGWJ0XYHJF kmip_poc % $VAULT_BIN secrets enable -path=mymount kv
Success! Enabled the kv secrets engine at: mymount/
(.venv) kevin.albertson@M-PGWJ0XYHJF kmip_poc % $VAULT_BIN kv put -mount mymount mypath mysecret=foobar
Success! Data written to: mymount/mypath
```

Follow the KMIP tutorial to enable the KMIP secrets engine.
https://learn.hashicorp.com/tutorials/vault/kmip-engine?in=vault/adp

Verify the KMIP server works with a PyKMIP client:
```
% python example_client_vault.py
created SecretData with UID=CV6WZY8yzIjK0q8EamrEjgUAKw6xOEsJ
activate SecretData CV6WZY8yzIjK0q8EamrEjgUAKw6xOEsJ
got SecretData with value b'\xe8\xb0\xdb\xb8H\x91\xad\x05\xbeJk\xba\xe9Z;\x07\x89\x12d\x12R\x86\xe3-\xceZo\x17\x06\xd2+\xc9Z\xe9\xaa\x0b\xb9\xbd\x1c\x17\xb9~\x8dg#\xa7\x82\xecl\x9c\x1a\xfaWn\xe5\x1cW\x8c\xe2\x9d\xeb\x8c\xcaTO\xd9\xc0!\xe9{\x86T\xb8\xdb\xa4J\x81\x14\xe1\x1c\x9a;\x95Z\xac:\xad>{\x14\x8fP>j\x19\xc7'
```

Verify the KMIP server works with the Go driver:
```
% ./test_with_godriver/run.sh 
~/code/kmip_poc/test_with_godriver ~/code/kmip_poc
CreateDataKey... begin
Created key with a UUID: 9810165bb6b24c0b852634929928d244
CreateDataKey... end
Encrypt... begin
Explicitly encrypted to ciphertext: {6 019810165bb6b24c0b852634929928d2440292cac8eece447c5139e070c985a3544ea39b467db29e05350440238092a6a988c4f855f4b617bf66042e45aa4262697b5b8eb777fdafcfc7b3935cbee691599d}
Encrypt... end
Decrypt... begin
Explicitly decrypted to plaintext: "test"
Decrypt... end
~/code/kmip_poc
```