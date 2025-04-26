import hashlib

def SHA_256(data, salt=b"0"):
    sha256 = hashlib.sha256()
    sha256.update(salt + data)
    return sha256.digest()
