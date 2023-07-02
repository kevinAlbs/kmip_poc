import socket
import ssl

port = 12345
"""
Use TLS 1.2 so session ticket is sent.
https://docs.python.org/3/library/ssl.html#ssl-session describes:
> Session tickets are no longer sent as part of the initial handshake and are handled differently. SSLSocket.session and SSLSession are not compatible with TLS 1.3.
"""
context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations(cafile="ca.pem")
conn: ssl.SSLSocket = context.wrap_socket(socket.socket(socket.AF_INET),
                                          server_hostname="localhost")
conn.connect(("localhost", port))
conn.write(b"foo")
assert not conn.session_reused
session = conn.session
conn.close()
# Connect again and reuse the session.
conn = context.wrap_socket(socket.socket(socket.AF_INET),
                           server_hostname="localhost",
                           session=session)
conn.connect(("localhost", port))
conn.write(b"foo")
assert conn.session_reused
conn.close()
