'''from pycrypto.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
from urllib import parse


# Public and private keys required for encryption
def create_rsa_key(password="123456"):
    key = RSA.generate(1024)
    encrypted_key = key.exportKey(passphrase=password, pkcs=8,
                                  protection="scryptAndAES128-CBC")

    privkey = encrypted_key
    pubkey = key.publickey().exportKey()
    return privkey, pubkey


# Decryption
def decrypt_data(data, priv_key, code="123456"):
    data = parse.unquote(data)
    data = base64.b64decode(data)
    priv_key = RSA.import_key(priv_key, passphrase=code)
    cipher_rsa = PKCS1_v1_5.new(priv_key)
    sentinel = None
    ret = cipher_rsa.decrypt(data, sentinel)
    return ret'''
