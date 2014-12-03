import sys
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto import Random

license = '{"expiration":1449031259,"id":"08f9e385-2ae3-4678-a12d-9f91de9e95c0","name":"Kris Barrett","nodes":[66002175764577,121375392182],"product":"Reflow Oven Controller"}'

key = RSA.importKey(open('privkey.pem').read())
h = SHA.new()
h.update(license)
signer = PKCS1_v1_5.new(key)
signature = signer.sign(h)

sys.stdout.write('signature = [')
for c in signature:
	sys.stdout.write(str(ord(c)))
	sys.stdout.write(', ')

sys.stdout.write(']\nlicense = \'')
sys.stdout.write(license)
sys.stdout.write('\'')