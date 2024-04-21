import hashlib
import base64

def one_time_encrypt(string: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    hash_value = hash_object.hexdigest()
    return hash_value

def encode(string: str) -> str:
    return base64.b64encode(string.encode()).decode()

def decode(string: str) -> str:
    return base64.b64decode(string.encode()).decode()
