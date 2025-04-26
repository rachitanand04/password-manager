from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

def encrypt(data,key):
    cipher = AES.new(key, AES.MODE_ECB)
    paddedData = pad(data, AES.block_size)
    return cipher.encrypt(paddedData)

def decrypt(data,key):
    cipher = AES.new(key, AES.MODE_ECB)
    paddedData = cipher.decrypt(data)
    return unpad(paddedData,AES.block_size)