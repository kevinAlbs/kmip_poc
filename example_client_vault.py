from kmip.pie.client import ProxyKmipClient, enums
from kmip.pie import objects
import kmip.core.enums
import os
import base64

PORT = 5696

client = ProxyKmipClient(
    hostname='127.0.0.1',
    port=PORT,
    cert='/Users/kevin.albertson/.hashicorp_vault/kmip_certs/cert.pem',
    key='/Users/kevin.albertson/.hashicorp_vault/kmip_certs/key.pem',
    ca='/Users/kevin.albertson/.hashicorp_vault/kmip_certs/ca.pem',
    ssl_version="PROTOCOL_TLSv1_2",
    config_file='/Users/kevin.albertson/code/kmip_poc/config/empty.cfg',
    kmip_version=enums.KMIPVersion.KMIP_1_2
)


def create_key():
    with client:
        uid = client.create(enums.CryptographicAlgorithm.AES, 128, operation_policy_name=None, name=None, cryptographic_usage_mask=[
                            enums.CryptographicUsageMask.ENCRYPT, enums.CryptographicUsageMask.DECRYPT])
        client.activate(uid)
        print(f"created and activated key with only encrypt usage: {uid}")


# Does not work on Hashicorp vault.
def encrypt_decrypt(uid):
    data = b'foo bar'
    encrypt_params = {
        'cryptographic_algorithm': enums.CryptographicAlgorithm.AES,
        'block_cipher_mode': enums.BlockCipherMode.CBC,
        'padding_method': enums.PaddingMethod.PKCS5,
        'random_iv': True
    }
    decrypt_params = {
        'cryptographic_algorithm': enums.CryptographicAlgorithm.AES,
        'block_cipher_mode': enums.BlockCipherMode.CBC,
        'padding_method': enums.PaddingMethod.PKCS5,
    }
    with client:
        ciphertext, iv = client.encrypt(data, uid, encrypt_params)
        print(f"encrypted to {ciphertext}")
        plaintext = client.decrypt(
            ciphertext, uid, decrypt_params, iv_counter_nonce=iv)
        print(f"decrypted to {plaintext}")

def get_keydata(uid):
    with client:
        key : objects.SymmetricKey = client.get(uid)
        print (len(key.value) * 8)
        print (key.value)

def describe_object (uid):
    with client:
        _, attrs = client.get_attributes(uid)
        for attr in attrs:
            print (attr)
        print ("")

def dump_objects ():
    uids = []
    with client:
        uids = client.locate()
    for uid in uids:
        describe_object (uid)

# encrypt_decrypt("6fEonxicpKw8f7S2o4dJPEB3BhyQkFod")
# describe_object ("7")
# dump_objects ()
# create_key ()
# get_keydata("nI1ClIv6j2Q3L6rvZxZ3MbD7zDUek8xx")

def createDataKey_flow ():
    # Create a 96 byte KEK.
    kek = os.urandom (96)
    
    # Hashicorp Vault supports only SymmetricKey and SecretData.
    with client:
        # TODO: Hashicorp Vault seems to require that KMIP names are unique.
        # kmip.pie.exceptions.KmipOperationFailure: OPERATION_FAILED: INVALID_FIELD - result reason: ResultReasonInvalidField; additional message: object with "scope_text_names" name of "Secret Data" already exists
        random_name = "unique_name_" + base64.b64encode (os.urandom(5)).decode("utf8")
        secretdata = objects.SecretData(kek, enums.SecretDataType.SEED, [
                                        enums.CryptographicUsageMask.ENCRYPT, enums.CryptographicUsageMask.DECRYPT], random_name)
        uid = client.register(secretdata)
        print(f"created SecretData with UID={uid}")

        client.activate (uid)
        print(f"activate SecretData {uid}")
        return uid


def encrypt_flow (uid):
    with client:
        secretdata = client.get (uid)
        # TODO Encrypt with the 96 byte 
        print (f"got SecretData with value {secretdata.value}")
        assert (len(secretdata.value) == 96)

def csfle_poc ():
    uid = createDataKey_flow ()
    encrypt_flow (uid)


# describe_object ("yZi4vK1PxoWBbndJTikl5Q4Mp8hWpnYw")

csfle_poc ()
