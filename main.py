import eel

from CryptoModule import keysFile
from base64 import b64encode, b64decode

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

KEYSFILE = keysFile()

eel.init('UI')

@eel.expose
def create_file(name, password):
    KEYSFILE.new(password, name)

@eel.expose
def login(path, password):
    return KEYSFILE._import(path, password)


# Friends Page #
@eel.expose
def get_friends_keys():
    return KEYSFILE.get_friends_pubKeys()

@eel.expose
def add_friend_key(name, key):
    return KEYSFILE.add_public_key(name, key)

@eel.expose
def del_friend_key(name):
    return KEYSFILE.del_public_key(name)


# Get Public Key Page #
@eel.expose
def get_messages_pubKey():
    return KEYSFILE.get_messages_pubKey()


# Encrypt Page #
@eel.expose
def _Encrypt(text, pubKey):
    try:
        key     = RSA.import_key(b64decode(pubKey.encode('utf-8')))
        cipher  = PKCS1_OAEP.new(key)

        cipherText = b64encode(cipher.encrypt(text.encode('utf-8'))).decode('utf-8')

        return cipherText
    
    except:
        return False


# Decrypt Page #
@eel.expose
def _Decrypt(cipherText):
    try:
        key     = KEYSFILE.get_messages_privKey()
        cipher  = PKCS1_OAEP.new(key)

        text    = cipher.decrypt(b64decode(cipherText.encode('utf-8'))).decode('utf-8')

        return text
    
    except:
        return False


eel.start('Main.html', size = (1000, 800))
