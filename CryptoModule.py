###########################
##  Crypto Module        ##
##  Version: 2.0.0       ##
##  By: DJI              ##
###########################

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA3_256

from base64 import b64encode, b64decode
from json import loads, dumps

import os


class Encryption():
    AES_MODE    = AES.MODE_CBC

    PKCS5_PAD   = lambda self, x: x + (16 - len(x) % 16) * chr(16 - len(x) % 16)
    PKCS5_UNPAD = lambda self, s: s[0:-ord(s[-1:])]

    def encryptAES(self, pass_hash, data):
        try:
            cipher_AES = AES.new(pass_hash, self.AES_MODE)

            ct_bytes = cipher_AES.encrypt(bytes(self.PKCS5_PAD(data), encoding="utf8")) # Шифрування AES

            iv = b64encode(cipher_AES.iv).decode('utf-8')
            ct = b64encode(ct_bytes).decode('utf-8')

            return str(f'{iv},{ct}')
        except:
            return False
    
    def decryptAES(self, pass_hash, data):
        try:
            data = data.split(",") # [0] IV; [1] CT

            cipher_AES = AES.new(pass_hash, self.AES_MODE, b64decode(data[0]))

            text = cipher_AES.decrypt(b64decode(data[1]))

            return self.PKCS5_UNPAD(text).decode("utf8")
        except:
            return False


class keysFile():

    OUTPUT_PATH     = str(os.environ['USERPROFILE'] + r'\\Desktop\\')

    RSA_PUB_KEY_TYPE    = "DER"
    RSA_PRIV_KEY_TYPE   = "DER"

    def _import(self, path, password):
        self.NOW_FILE   = {}
        self.path       = path

        pass_hash       = SHA3_256.new(data = password.encode('utf-8')).digest()

        try:
            with open(path, 'r') as File: # Відкриваємо файл з ключами
                raw_data = str(File.read())

                File.close()
            
            data = Encryption().decryptAES(pass_hash, raw_data)

            if data == False : return False

            self.NOW_FILE = loads(data)

        except:
            return False # Якщо щось не так повертаємо False

        return True

    def save(self):
        data        = dumps(self.NOW_FILE) # Перетворення dict в Json Str
        pass_hash   = bytes.fromhex(self.NOW_FILE['password_hash']) # Перетворив пароль з hex в байти

        with open(self.path, 'w') as File:
            enc_data = Encryption().encryptAES(pass_hash, data)

            if enc_data == False : return False

            File.write(enc_data)
            File.close()

    def new(self, password, nickName):
        FILE_STRUCTURE  = {}
        pass_hash       = SHA3_256.new(data = password.encode('utf-8')).hexdigest()

        FILE_STRUCTURE['nickName']                   = str(nickName)
        FILE_STRUCTURE['password_hash']              = str(pass_hash)

        FILE_STRUCTURE['friends_public_keys']        = []
        FILE_STRUCTURE['cryptocurrency_private_keys']= []
        FILE_STRUCTURE['RSA_private_keys']           = {}
        FILE_STRUCTURE['TelegramBot']                = {'api_id': '', 'api_hash': ''} # Інформація для телеграм бота

        pass_hash = bytes.fromhex(pass_hash) # Перетворив пароль з hex в байти

        # ГЕНЕРАЦІЯ RSA 2048 КЛЮЧІВ І ЗАПИС ДО СТРУКТУРИ #
        # FILE_STRUCTURE['RSA_private_keys']['files']     = b64encode(RSA.generate(2048).export_key('DER')).decode('utf-8')
        FILE_STRUCTURE['RSA_private_keys']['messages']  = b64encode(RSA.generate(2048).export_key(self.RSA_PRIV_KEY_TYPE, pkcs=8)).decode('utf-8')
        # FILE_STRUCTURE['RSA_private_keys']['other']     = b64encode(RSA.generate(2048).export_key('DER')).decode('utf-8')

        FILE_STRUCTURE  = dumps(FILE_STRUCTURE) # Перетворення dict в Json String

        # ЗАПИС ВСЬОГО В ФАЙЛ #
        with open(self.OUTPUT_PATH + f'{str(nickName)}.keys', 'w') as File:
            enc_data = Encryption().encryptAES(pass_hash, FILE_STRUCTURE)

            if enc_data == False : return False

            File.write(enc_data)
            File.close()

    def add_public_key(self, name, pubKey):
        for i in self.NOW_FILE['friends_public_keys']:
            if name == i['nickname']:
                return False

        self.NOW_FILE['friends_public_keys'].append({'nickname': name, 'key': pubKey})
        self.save()

    def del_public_key(self, name):
        a = 0 # Індекс масиву

        for i in self.NOW_FILE['friends_public_keys']:
            if name == i['nickname']:
                del self.NOW_FILE['friends_public_keys'][a]

                self.save()
                return True     

            a += 1

        return False

    def change_name(self, newName):
        self.NOW_FILE['nickName'] = str(newName)
        self.save()

    def change_password(self, oldPass, newPass):
        oldPass_hash = SHA3_256.new(data = oldPass.encode('utf-8')).hexdigest()

        if oldPass_hash == self.NOW_FILE['password_hash']:
            newPass_hash = SHA3_256.new(data = newPass.encode('utf-8')).hexdigest()

            self.NOW_FILE['password_hash'] = newPass_hash
            self.save()

        else:
            return False

    def add_cryptocurrency_private_key(self, Ctype, name, privKey): #Not Used
        self.NOW_FILE['cryptocurrency_private_keys'].append({'type': Ctype, 'name': name, 'key': privKey})
        self.save()

    def del_cryptocurrency_private_key(self, name): #Not Used
        a = 0 # Індекс

        for i in self.NOW_FILE['cryptocurrency_private_keys']:
            if name == i['name']:
                del self.NOW_FILE['cryptocurrency_private_keys'][a]
                break
            a += 1

        self.save()

    def get_nickName(self):
        return self.NOW_FILE['nickName']

    def get_files_privKey(self): #Not Used
        raw_key = b64decode(self.NOW_FILE['RSA_private_keys']['files'].encode('utf-8')) # Перетворили RSA ключ з b64
        key     = RSA.import_key(raw_key)

        return key

    def get_messages_privKey(self):
        raw_key = b64decode(self.NOW_FILE['RSA_private_keys']['messages'].encode('utf-8')) # Перетворили RSA ключ з b64
        key     = RSA.import_key(raw_key)

        return key
    
    def get_messages_pubKey(self):
        rsa = self.get_messages_privKey()

        return b64encode(rsa.publickey().export_key(self.RSA_PUB_KEY_TYPE, pkcs=8)).decode("utf8")

    def get_other_privKey(self): #Not Used
        raw_key = b64decode(self.NOW_FILE['RSA_private_keys']['other'].encode('utf-8')) # Перетворили RSA ключ з b64
        key     = RSA.import_key(raw_key)

        return key

    def get_friends_pubKeys(self):
        return self.NOW_FILE['friends_public_keys']

    def get_cryptocurrency_privKeys(self): #Not Used
        return self.NOW_FILE['cryptocurrency_private_keys']

    ### Telegram User Bot func ###

    def set_telegram_api(self, id, hash):
        self.NOW_FILE['TelegramBot']['api_id']   = str(id)
        self.NOW_FILE['TelegramBot']['api_hash'] = str(hash)

        self.save()

    def get_telegram_api_id(self):
        return self.NOW_FILE['TelegramBot']['api_id']
    
    def get_telegram_api_hash(self):
        return self.NOW_FILE['TelegramBot']['api_hash']

    ### Password Check Modal ###
    def get_password_hash(self):
        return self.NOW_FILE['password_hash']