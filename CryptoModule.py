from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA3_256

from base64 import b64encode, b64decode




class keysFile():

    def new(self, password, nickName):
        pass

    def _import(self, path):
        pass

    def add_public_key(self, name, pubKey):
        pass

    def del_public_key(self, name):
        pass

    def change_name(self, newName):
        pass

    def change_password(self, oldPass, newPass):
        pass

    def add_cryptocurrency_private_key(self, type, privKey):
        pass

    def del_cryptocurrency_private_key(self, id):
        pass

    def get_files_privKey(self):
        pass

    def get_messages_privKey(self):
        pass

    def get_other_privKey(self):
        pass
