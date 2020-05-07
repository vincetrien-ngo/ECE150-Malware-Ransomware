import sys
import base64

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

masterkey = RSA.importKey(open("master_private.pem", "rb").read())
pub = masterkey.publickey()

bcrypt = open("info.bcrypt", "r").read()
lines = bcrypt.split("\n")

# Check if we have the right RSA key

for l in lines:
	if not l.startswith("Encrypted RSA public key: "):
		continue
	k = l.split(": ")[1].strip().encode()
	if k != base64.b64encode(pub.exportKey('PEM')):
		print("Public keys don't match!")
		sys.exit(1)

# Attempt to decrypt all Salsa20 keys

dec = False
cipher = PKCS1_OAEP.new(masterkey)

print('keys=[')

for l in lines:
	if dec:
		try:
			txt = cipher.decrypt(base64.b64decode(l))
		except:
			continue
		a = txt.split(b".", 2)
		ext = "." + a[1].decode()
		key = a[2]
		print("('{}', {}),".format(ext, key))
	if "Encrypted file-specific keys:" in l:
		dec = True
print("]")
