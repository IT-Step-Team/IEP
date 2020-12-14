import eel

from CryptoModule import keysFile
from base64 import b64encode

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
    rsa = KEYSFILE.get_messages_privKey()

    return b64encode(rsa.publickey().export_key('DER')).decode('utf-8')



eel.start('Main.html', size = (1000, 800))
