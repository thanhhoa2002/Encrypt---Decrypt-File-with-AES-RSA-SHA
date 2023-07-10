import hashlib

def sha1_hash_string(message):
    hasher = hashlib.sha1()
    hasher.update(message.encode('utf-8'))
    hash_value = hasher.hexdigest()
    return hash_value

def sha256_hash_string(message):
    hasher = hashlib.sha256()
    hasher.update(message.encode('utf-8'))
    hash_value = hasher.hexdigest()
    return hash_value