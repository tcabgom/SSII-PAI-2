# serversocket.py
import hashlib
import datetime
import os
import platform
from plyer import notification
import socket
import keygenerator
import struct

HOST = "127.0.0.1"
PORT = 3030
NONCE_DB_FILE = "nonce_database.txt"
LOG = "logs/error_log.txt"


def send_notification(title, message):
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

def create_nonce_database():
    nonce_database = set()

    if os.path.exists(NONCE_DB_FILE):
        with open(NONCE_DB_FILE, "r") as file:
            for line in file:
                nonce_database.add(line.strip())

    return nonce_database

nonce_db = create_nonce_database()

def receive_transaction(data):
    origin_account, destination_account, amount, message_hash, nonce = struct.unpack('>iii32s32s', data)
    #print(f"Received transaction data: {origin_account}, {destination_account}, {amount}, {message_hash}, {nonce}")
    communication_key = keygenerator.DUMMY_SIMETRIC_KEY
    result = check_message_integrity((origin_account, destination_account, amount), communication_key, nonce, message_hash, nonce_db)
    if result:
        return "Transaction successful"
    else:
        return "Transaction failed"


def save_nonce_to_database(nonce):
    with open(NONCE_DB_FILE, "a") as file:
        file.write(f"{nonce}\n")

def verify_nonce(nonce, nonce_database):
    # Verificación del nonce
    print(f"Verifying nonce: {nonce}")
    print(f"Nonce database: {nonce_database}")
    if nonce not in nonce_database:
        nonce_database.add(nonce)
        save_nonce_to_database(nonce)  # Guardar el nuevo nonce
        return True
    else:
        return False


def log_error(message, reason):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")
        log_file.write(f"Reason: {reason}\n\n")


def check_message_integrity(message, communication_key, nonce, received_hash, nonce_database = nonce_db):
    #print(f"Received transaction data: {message[0]}, {message[1]}, {message[2]}, {communication_key}, {nonce}")
    expected_hash = keygenerator.generate_key((message[0].to_bytes(4, byteorder='big'), 
                                               message[1].to_bytes(4, byteorder='big'), 
                                               message[2].to_bytes(4, byteorder='big')), 
                                               communication_key, nonce)
    is_valid = True

    if expected_hash != received_hash:
        is_valid = False
        error_message = f"Error: Message integrity check failed\n"\
                        f"Expected Message Key: {expected_hash}\n"\
                        f"Received Message Key: {received_hash}\n"\

        log_error(error_message, "Key or Hash mismatch")
        send_notification("Integrity Check Failed", "Message integrity check failed. Check error_log.txt for details.")

    if not verify_nonce(nonce, nonce_database):
        is_valid = False
        error_message = f"Error: Message integrity check failed\n"\
                        f"Nonce verification failed\n"\
                        f"Expected Nonce: {nonce}\n"\
                        f"Received Nonce: {nonce}\n"

        log_error(error_message, "Nonce verification failed")
        send_notification("Integrity Check Failed", "Message integrity check failed. Check error_log.txt for details.")

    if is_valid:
        send_notification("Integrity Check Passed", "Message integrity check passed successfully.")
    return is_valid


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        if not os.path.exists(NONCE_DB_FILE):
            open(NONCE_DB_FILE, 'w').close()

        while True:
            data = conn.recv(1024)
            if not data:
                break
            result = receive_transaction(data)
            conn.sendall(result.encode())
            