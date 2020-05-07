#!/usr/bin/python3
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

print("Generating new master key, please wait...")

random_generator = Random.new().read
key = RSA.generate(2048, random_generator)

print("Key generated, saving to files...")

open('master_public.pem', 'wb').write(key.publickey().exportKey('PEM'))
open('master_private.pem', 'wb').write(key.exportKey('PEM'))

print("Done! Your public key is:")
print("(n, e): ({}, {})".format(key.n, key.e))

print("Copy the following line in your code: ")
print("masterkey = RSA.importKey(base64.b64decode(b\"{}\"))".format(base64.b64encode(key.publickey().exportKey('PEM')).decode()))
