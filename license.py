import sys
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

# License
license_details = '{"expiration":1449031259,"id":"08f9e385-2ae3-4678-a12d-9f91de9e95c0","host":"s3.amazonaws.com","path":"/reflow-licenses/","name":"Kris Barrett","nodes":[66002175764577,121375392182],"product":"Reflow Oven Controller"}'

# Encryption key
encryption_key = b''
for i in [127, 194, 34, 166, 139, 10, 252, 13, 12, 33, 62, 156, 32, 156, 23, 161]:
	encryption_key += chr(i)
iv = Random.new().read(AES.block_size)
cipher = AES.new(encryption_key, AES.MODE_CFB, iv)

# Signature
private_key = RSA.importKey(open('privkey.pem').read())
public_key = open('pubkey.pem').read()
h = SHA.new()
h.update(license_details)
signer = PKCS1_v1_5.new(private_key)
signature = signer.sign(h)

# license structure:
# iv - 16 bytes
# encrypted payload:
#   iv - 16 bytes
#   signature
#   license details


payload = b''

for c in iv:
	payload += c

for c in signature:
	payload += c

for c in license_details:
	payload += c

encrypted_payload = iv + cipher.encrypt(payload)

f = open('license', 'w')
for c in encrypted_payload:
	f.write(c)

# sys.stdout.write('encrypted_payload = [')
# for c in encrypted_payload:
# 	sys.stdout.write(str(ord(c)))
# 	sys.stdout.write(', ')
# print(']')

cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
encrypted_public_key = iv + cipher.encrypt(public_key)
sys.stdout.write('encrypted_public_key = [')
for c in encrypted_public_key:
	sys.stdout.write(str(ord(c)))
	sys.stdout.write(', ')
print(']')



