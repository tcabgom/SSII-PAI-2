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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(ask_user_account_number())
    data = s.recv(1024)

print(f"Received {data!r}")
