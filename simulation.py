from clientsocket import transaction_without_attack
from clientsocket_modification_attack import modification_attack
from clientsocket_replay_attack import replay_attack
import random
import struct
import socket
from clientsocket import generate_nonce


def receive_server_response(data):
    origin_account, destination_account, accepted, message_hash, nonce = struct.unpack('>iii32s32s', data)

def random_attack(HOST, PORT, nonce, receive_server_response, s):
    # Selecciona un ataque aleatorio
    attack_functions = [replay_attack, modification_attack, transaction_without_attack]
    random_attack_func = random.choice(attack_functions)
    
    if (random_attack == transaction_without_attack):
        NUM_INTEGROS = NUM_INTEGROS + 1
    
    return random_attack_func(HOST, PORT, nonce, (10, 20, 30), receive_server_response, s)

def calculate_integrity_KPI(num_transactions, num_integras):
    return (num_integras / num_transactions) * 100


HOST = "127.0.0.1"  # Dirección del servidor
PORT = 3030  # Puerto del servidor
NUM_TRANSACTIONS = 100  # Número de transacciones a realizar
NUM_INTEGROS = 0  # Inicialmente, ningún mensaje es íntegro

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Iterar a través del número de transacciones especificado
        for _ in range(NUM_TRANSACTIONS):
            nonce = generate_nonce()
            random_attack(HOST, PORT, nonce, receive_server_response, s)
            

integrity_KPI = calculate_integrity_KPI(NUM_TRANSACTIONS, NUM_INTEGROS)
print(f"El KPI de integridad es: {integrity_KPI:.2f}%")