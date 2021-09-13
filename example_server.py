from kmip.services.server import KmipServer
import logging

PORT = 5696

if __name__ == '__main__':
    server = KmipServer(
        hostname="localhost",
        port=PORT,
        certificate_path="/Users/kevin.albertson/code/kmip_poc/config/server_certificate.pem",
        key_path="/Users/kevin.albertson/code/kmip_poc/config/server_key.pem",
        ca_path="/Users/kevin.albertson/code/kmip_poc/config/root_certificate.pem",
        auth_suite=None,
        config_path='/Users/kevin.albertson/code/kmip_poc/config/server_config.cfg',
        log_path='/Users/kevin.albertson/code/kmip_poc/config/pykmip.log',
        policy_path=None,
        enable_tls_client_auth=None,
        tls_cipher_suites=None,
        logging_level=logging.DEBUG,
        live_policies=False,
        database_path='/Users/kevin.albertson/code/kmip_poc/config/pykmip.db'
    )

    with server:
        print (f"Listening on port {PORT}")
        server.serve()
