keys=[
('.txt', b'\x8e\xe5\x05\xed&x\n\x12\xf2\xae<\xc5CB.,g\xf0\xc20\xc4\xbf\x12\x14\x8e\x1cJ \x11\x93\x8cO'),
('.pdf', b'\xf3\x99#\xceb\xdcm>\xcc<\xf6\xde\xac<y\x03\x85:\xdeC\x0e\xa4\xbe\xd6@\xf5\xfdL\xba\xbf4\x89'),
]

import os

import Crypto
from Crypto.Cipher import Salsa20

# fs_root = "/" - if the user is root
# fs_root = os.path.expanduser("~") - if the user doesn't have root priviledges
fs_root = os.path.join(os.path.expanduser("~"), "test") # for testing purposes

def getFiles(dir, ext=".txt.enc"):
	fs = os.listdir(dir)
	files = list()
	for f in fs:
		path = os.path.join(dir, f)
		if os.path.isdir(path):
			files = files + getFiles(path, ext)
		else:
			if path.endswith(ext):
				files.append(path)
	return files

def decryptFile(file, key):
	#try:
	print("Decrypting {}...".format(file))
	enc = open(file, 'rb').read()
	nonce = enc[:8]
	ciphertext =enc[8:]
	cipher = Salsa20.new(key=key, nonce=nonce)
	plaintext = cipher.decrypt(ciphertext)
	open("{}".format(file.replace(".enc", "")), "wb").write(plaintext)
	os.remove(file)
	#except:
	#	print("Could not decrypt {}!".format(file))

def decryptFileExtension(ext, key):
	global fs_root
	files = getFiles(fs_root, ext + ".enc")
	for file in files:
		decryptFile(file, key)

def main():
	global keys
	global fs_root
	for ext, key in keys:
		decryptFileExtension(ext, key)
	# Cleanup
	os.remove(os.path.join(fs_root, 'info.bcrypt'))
	os.remove(os.path.join(fs_root, 'Desktop', 'OPEN_ME.txt'))

if __name__ == "__main__":
	main()
