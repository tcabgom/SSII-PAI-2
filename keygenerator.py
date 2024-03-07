import hashlib

DUMMY_SIMETRIC_KEY = bytes.fromhex("0123456789")

def generate_key(message, communication_key, nonce):
    message_str1 = str(message[0])
    message_str2 = str(message[1])
    message_str3 = str(message[2])
    communication_key_str = str(communication_key)
    nonce_str = str(nonce)

    combined_data = message_str1 + message_str2 + message_str3 + communication_key_str + nonce_str
    key = hashlib.sha256(combined_data.encode()).digest()
    return key
