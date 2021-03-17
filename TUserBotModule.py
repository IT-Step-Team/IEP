from pyrogram import Client, filters
from CryptoModule import keysFile
from base64 import b64encode, b64decode

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



class userBot():
    def __init__(self, api_id, api_hash, KEYSFILE):
        self.app = Client("TelegramUserBot", api_id=api_id, api_hash=api_hash)

        @self.app.on_message(filters.command("help", prefixes="/") & filters.me)
        def commands(_, msg):
            msg.edit(f"**Commands:\n** \n``` /pubKey``` - returns your public key. \n``` /autoEnc [message]``` - Detecting your friend public key end enrypting message. \n``` /enc [friend name] [message]``` - With friend public key encrypting message. \n``` /friendPubKey [friend name]``` - Returns friend public key. \n``` /cryptoStop``` - Stopping this bot.")

        @self.app.on_message(filters.command("pubKey", prefixes="/") & filters.me)
        def show_pubKey(_, msg):
            me  = self.app.get_me()
            key = b64encode(KEYSFILE.get_messages_privKey().publickey().export_key('DER')).decode('utf-8')

            msg.edit(f"**{me.username}'s Public key:** ```\n{key}```")
        
        @self.app.on_message(filters.command("autoEnc", prefixes="/") & filters.me)
        def auto_encrypt(_, msg):
            keys = KEYSFILE.get_friends_pubKeys()

            for i in keys:
                if i["nickname"] == msg.chat.username:
                    key     = RSA.import_key(b64decode(i["key"].encode('utf-8')))
                    cipher  = PKCS1_OAEP.new(key)
                    text    = msg.text[9:]

                    cipherText = b64encode(cipher.encrypt(text.encode('utf-8'))).decode('utf-8')

                    msg.edit(f"**Enrypted message for {msg.chat.username}:** ```\n{cipherText}```")
                    break
        
        @self.app.on_message(filters.command("enc", prefixes="/") & filters.me)
        def encrypt(_, msg):
            arr  = str(msg.text).split(" ")
            keys = KEYSFILE.get_friends_pubKeys()

            for i in keys:
                if i["nickname"] == arr[1]:
                    key     = RSA.import_key(b64decode(i["key"].encode('utf-8')))
                    cipher  = PKCS1_OAEP.new(key)
                    text    = msg.text[msg.text.find(arr[1]) + len(arr[1]) + 1:]

                    cipherText = b64encode(cipher.encrypt(text.encode('utf-8'))).decode('utf-8')

                    msg.edit(f"**Enrypted message for {arr[1]}:** ```\n{cipherText}```")
                    break   
                 
 
        @self.app.on_message(filters.command("friendPubKey", prefixes="/") & filters.me)
        def friend_pubKey(_, msg):
            arr  = str(msg.text).split(" ")
            keys = KEYSFILE.get_friends_pubKeys()

            for i in keys:
                if i["nickname"] == arr[1]:
                    msg.edit(f"**{arr[1]}'s Public key:** ```\n{i['key']}```")
                    break     

        @self.app.on_message(filters.command("cryptoStop", prefixes="/") & filters.me)
        def bot_stop():
            self.app.stop()

    def start(self):
        self.app.run()
