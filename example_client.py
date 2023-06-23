from kmip.pie.client import ProxyKmipClient, enums
from kmip.pie import objects
import kmip.core.enums

PORT = 5696

client = ProxyKmipClient(
    hostname='localhost',
    port=PORT,
    cert='/Users/kevin.albertson/code/kmip_poc/config/client_certificate_jane_doe.pem',
    key='/Users/kevin.albertson/code/kmip_poc/config/client_key_jane_doe.pem',
    ca='/Users/kevin.albertson/code/kmip_poc/config/root_certificate.pem',
    config_file='/Users/kevin.albertson/code/kmip_poc/config/client_config.cfg',
    kmip_version=enums.KMIPVersion.KMIP_1_2
)


def create_key():
    with client:
        uid = client.create(enums.CryptographicAlgorithm.AES, 128, None, "mykey", [
                            enums.CryptographicUsageMask.ENCRYPT, enums.CryptographicUsageMask.DECRYPT])
        client.activate(uid)
        print(f"created and activated key with only encrypt usage: {uid}")


def encrypt_decrypt():
    uid = create_key()
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


def describe_object(uid):
    with client:
        _, attrs = client.get_attributes(uid)
        for attr in attrs:
            print(attr)
        print("")


def dump_objects():
    uids = []
    with client:
        uids = client.locate()
    for uid in uids:
        describe_object(uid)


# encrypt_decrypt()
# describe_object ("7")
dump_objects()
