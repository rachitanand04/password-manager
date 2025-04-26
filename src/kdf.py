from Crypto.Protocol.KDF import scrypt

def KDF(password, salt):
    key = scrypt(password, salt, 16, N=2**14, r=8, p=1)
    return key
