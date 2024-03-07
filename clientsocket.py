# clientsocket.py

import socket
import tkinter as tk
from tkinter import simpledialog
import keygenerator
import secrets

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

def generate_nonce():
    return b'\xa1\x1e\x0b\xf0\xdf\xb8uL\r%\xf3\x1c\xf4\x88\xea\x89h\r\x10\x06u\xf5zG\xd8\x07\xf8\xe57\xee-\x8b' #secrets.token_bytes(32)

def ask_user_account_number():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askinteger("Input", "Introduce cuenta origen:")
    return user_input


def ask_transation_data():
    root = tk.Tk()
    root.withdraw()
    user_input1 = simpledialog.askinteger("Input", "Introduce cuenta origen:")
    user_input2 = simpledialog.askinteger("Input", "Introduce cuenta destino:")
    user_input3 = simpledialog.askinteger("Input", "Introduce cantidad:")
    return user_input1, user_input2, user_input3


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

print(f"Received {data!r}")
