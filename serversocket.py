# serversocket.py

import socket
import keygenerator

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


def check_message_integrity(message, communication_key, nonce, received_message_key):

    expected_message_key = keygenerator.generate_key(message, communication_key, nonce)

    if expected_message_key != received_message_key:
        # TODO
        pass

    if not verify_nonce(nonce):
        # TODO
        pass

    # TODO


def create_nonce_database():
    pass


def verify_nonce(nonce):
    pass
