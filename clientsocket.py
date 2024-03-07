# clientsocket.py

import platform
import socket
import struct
import tkinter as tk
from tkinter import simpledialog
from plyer import notification
import keygenerator
import secrets

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

def generate_nonce():
    return secrets.token_bytes(32)


def ask_transation_data():
    root = tk.Tk()
    root.withdraw()
    user_input1 = simpledialog.askinteger("Input", "Introduce cuenta origen:")
    user_input2 = simpledialog.askinteger("Input", "Introduce cuenta destino:")
    user_input3 = simpledialog.askinteger("Input", "Introduce cantidad:")
    return user_input1, user_input2, user_input3


def send_notification(title, message):
    # TODO: ESTE CODIGO ESTÁ DUPLICADO. EN SERVERSOCKET, SOLUCIONAR
    if platform.system() == "Windows":
        notification.notify(
            title=title,
            message=message,
        )
    elif platform.system() == "Linux":
        notification.notify(
            title=title,
            message=message,
            app_name="Integrity Checker",
        )

def receive_server_response(data):
    origin_account, destination_account, accepted, message_hash, nonce = struct.unpack('>iii32s32s', data)


def check_response_integrity(origin_account, destination_account, accepted, received_hash, expected_nonce, received_nonce):

    expected_hash = keygenerator.generate_key((origin_account.to_bytes(4, byteorder='big'), 
                                               destination_account.to_bytes(4, byteorder='big'), 
                                               accepted.to_bytes(4, byteorder='big')), 
                                               keygenerator.DUMMY_SIMETRIC_KEY, nonce)
    is_valid = True

    if expected_hash != received_hash:
        # The hash must be the same as the one calculated by the server
        is_valid = False
        error_message = f"Error: Message integrity check failed\n"\
                        f"Expected Message Key: {expected_hash}\n"\
                        f"Received Message Key: {received_hash}\n"\
        # TODO Notificacion de error

    if expected_nonce != received_nonce:
        # The nonce must be the same as the one sent by the client before
        is_valid = False
        error_message = f"Error: Message integrity check failed\n"\
                        f"Nonce verification failed\n"\
                        f"Expected Nonce: {nonce}\n"\
                        f"Received Nonce: {nonce}\n"
        # TODO Notificacion de error

    if is_valid:
        # TODO Notificacion de transaccion exitosa. Mover send_notification de serversocket.py a keygenerator.py
        #send_notification("Integrity Check Passed", "Message integrity check passed successfully.")
        pass
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    user_input1, user_input2, user_input3 = ask_transation_data()

    origin_account = user_input1.to_bytes(4, byteorder='big')
    destination_account = user_input2.to_bytes(4, byteorder='big')
    amount = user_input3.to_bytes(4, byteorder='big')
    nonce = generate_nonce()
    message_key = keygenerator.generate_key((origin_account, destination_account, amount), keygenerator.DUMMY_SIMETRIC_KEY, nonce)

    s.sendall(origin_account+destination_account+amount+message_key+nonce)
    data = s.recv(1024)
    receive_server_response(data)


print(f"Received {data!r}")
