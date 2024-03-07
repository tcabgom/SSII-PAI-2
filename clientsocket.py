# clientsocket.py

import socket
import tkinter as tk
from tkinter import simpledialog

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server


def ask_user_account_number():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring("Input", "Introduce cuenta origen:")
    return user_input


def make_transaction():
    root = tk.Tk()
    root.withdraw()
    # Necesita mejorar. Poner validadores y quizas la cuenta de origen pedirla al principio en la otra funcion
    user_input1 = simpledialog.askstring("Input", "Introduce cuenta origen:")
    user_input2 = simpledialog.askstring("Input", "Introduce cuenta destino:")
    user_input3 = simpledialog.askstring("Input", "Introduce cantidad:")
    return user_input1, user_input2, user_input3


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(ask_user_account_number())
    data = s.recv(1024)

print(f"Received {data!r}")
