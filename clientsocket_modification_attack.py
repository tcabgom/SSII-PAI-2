import socket
import tkinter as tk
from tkinter import simpledialog
import keygenerator
from integrity_functions import *

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

def ask_transation_data():
    root = tk.Tk()
    root.withdraw()
    user_input1 = simpledialog.askinteger("Input", "Introduce cuenta origen:")
    user_input2 = simpledialog.askinteger("Input", "Introduce cuenta destino:")
    user_input3 = simpledialog.askinteger("Input", "Introduce cantidad:")
    return user_input1, user_input2, user_input3
    

def modification_attack(HOST, PORT, nonce, ask_transation_data, receive_server_response, s):
    s.connect((HOST, PORT))
    user_input1, user_input2, user_input3 = ask_transation_data()

    origin_account = user_input1.to_bytes(4, byteorder='big')
    destination_account = user_input2.to_bytes(4, byteorder='big')
    amount = user_input3.to_bytes(4, byteorder='big')
    
    message_key = keygenerator.generate_key((origin_account, destination_account, amount), keygenerator.DUMMY_SIMETRIC_KEY, nonce)

    # Se modifica el contenido de la transaccion (modification attack)
    value_to_inject = 20
    s.sendall(origin_account+destination_account+value_to_inject.to_bytes(4, byteorder='big')+message_key+nonce)
    data = s.recv(1024)
    receive_server_response(data)
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    nonce = generate_nonce()
    data = modification_attack(HOST, PORT, nonce, ask_transation_data, receive_server_response, s)


print(f"Received {data!r}")