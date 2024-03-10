import struct
import platform
from plyer import notification
import keygenerator
import secrets

NONCE = 0


def generate_nonce():
    NONCE = secrets.token_bytes(32)
    return NONCE


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
                                               keygenerator.DUMMY_SIMETRIC_KEY, NONCE)
    is_valid = True

    if expected_hash != received_hash:
        # The hash must be the same as the one calculated by the server
        is_valid = False
        error_message = f"Error: Message integrity check failed\n"\
                        f"Expected Message Key: {expected_hash}\n"\
                        f"Received Message Key: {received_hash}\n"\
        
        send_notification("Integrity error", error_message)

    if expected_nonce != received_nonce:
        # The nonce must be the same as the one sent by the client before
        is_valid = False
        error_message = f"Error: Message integrity check failed\n"\
                        f"Nonce verification failed\n"\
                        f"Expected Nonce: {NONCE}\n"\
                        f"Received Nonce: {NONCE}\n"
                        
        send_notification("Integrity error", error_message)

    if is_valid:
        send_notification("Transaction accepted", "The transition has been successfully completed without any integrity issues")