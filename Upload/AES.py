import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256

# from Crypto.Cipher import AES
# import os
import random
import struct


 
def decrypt_file(key, filename, chunk_size=24*1024):
    output_filename = os.path.splitext(filename)[0]
    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)
 
 
def encrypt_file(key, filename, chunk_size=64*1024):
    output_filename = filename + '.encrypted'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as inputfile:
        with open(output_filename, 'wb') as outputfile:
            outputfile.write(struct.pack('<Q', filesize))
            outputfile.write(iv)
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outputfile.write(encryptor.encrypt(chunk))
def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)
    # outfile=None
	with open(filename, 'rb') as infile:#rb means read in binary
		with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk)%16 != 0:
					chunk += b' '*(16-(len(chunk)%16))

				outfile.write(encryptor.encrypt(chunk))
	return outputFile
	
def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename
	# filesize = int(infile.read(16))
	outputFile = os.path.splitext(filename)[0]
	with open(filename, 'rb') as infile:
		
		filesize=struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		IV = infile.read(16)

		decryptor= AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

def Main():
	choice = input("Would you like to (E)encrypt or (D)Decrypt ")

	if choice == 'E':
		filename = input("File to encrypt: ")
		password = input("Password: ")
		encrypt(getKey(password), filename)
		print('Done.')
	elif choice == 'D':
		filename = input("File to decrypt: ")
		password = input("Password: ")
		decrypt(getKey(password),filename)
		print("Done.")

	else:
		print("No option selected, closing...")


# Main()