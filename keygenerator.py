

DUMMY_SIMETRIC_KEY = "0123456789abcdef"

def generate_key(message, communication_key, nonce):
    message_string = message[0]+message[1]+message[2]+communication_key+nonce
    key = message_string   # Hay que hashear
    return key
