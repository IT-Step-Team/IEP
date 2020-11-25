from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from base64 import b64encode, b64decode

key = RSA.generate(2048)

print(b64encode(key.export_key('DER')).decode('utf-8'))
print()

print(b64encode(key.publickey().export_key('DER')).decode('utf-8'))

cipher = PKCS1_OAEP.new(key)

print()

data = b64encode(cipher.encrypt(b'hellow')).decode('utf-8')
# data = bytes.hex(cipher.encrypt(b'hellow'))
print(data)

print()
print(cipher.decrypt(b64decode(data.encode('utf-8'))))







# from base64 import b64encode, b64decode
# from Crypto.Cipher import AES
# from Crypto.Hash import SHA3_256

# data = b"secret"

# #3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392
# #b'38\xbeiOP\xc5\xf38\x81I\x86\xcd\xf0hdS\xa8\x88\xb8OBMy*\xf4\xb9 #\x98\xf3\x92'
# key = SHA3_256.new(data = b'hello').hexdigest()

# # bytes.fromhex()

# # key = bytes.fromhex(key)
# # key = key.hex()

# cipher = AES.new(key, AES.MODE_CFB)

# ct_bytes = cipher.encrypt(data)

# iv = b64encode(cipher.iv).decode('utf-8')
# ct = b64encode(ct_bytes).decode('utf-8')

# result = [iv, ct]

# print(result)
