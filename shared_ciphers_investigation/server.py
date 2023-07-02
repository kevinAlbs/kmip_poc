import socket
import ssl
import platform

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile="ca.pem")
context.load_cert_chain(certfile="server.pem")

port = 12345
bindsocket = socket.socket()
bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bindsocket.bind(("localhost", port))
bindsocket.listen(5)

print("Python version: {}".format(platform.python_version()))
print("server listening on port {}".format(port))
while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream: ssl.SSLContext.sslsocket_class = context.wrap_socket(
        newsocket, server_side=True, do_handshake_on_connect=True)
    print("server got connection on address: {}".format(fromaddr))
    print("server shared ciphers: {}".format(connstream.shared_ciphers()))
    print("server session reused? {}".format(connstream.session_reused))
    data = connstream.recv(1024)
    while data:
        print("server got data {}".format(data))
        data = connstream.recv(1024)
    print("server finished with client")
    connstream.close()
