import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import argparse
from random import randint
from utils_demo import *


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Setup for Bruteforce attack against randomized AES-128-CTR.')
    parser.add_argument('-n', type=int,
                        help='Effective key length in bytes.', default=3)
    parser.add_argument('-m1', type=str,
                        help='Plaintext1 file input name.', default="files/m1.txt")
    parser.add_argument('-m2', type=str,
                        help='Plaintext2 file input name.', default="files/m2.txt")
    parser.add_argument('-m3', type=str,
                        help='Plaintext3 file input name.', default="files/m3.txt")

    parser.add_argument('-c1', type=str, help='cipher text1  file input name.', default="files/c1.bin")
    parser.add_argument('-c2', type=str, help='cipher text2 file input name.', default="files/c2.bin")
    parser.add_argument('-c3', type=str, help='cipher text3 file input name.', default="files/c3.bin")
    args = parser.parse_args()
    #The input value for brute force attack in bits. 16 bits is equal to 2 bytes.
    length_postfix = args.n * 8
    #Reading plaintexts from files. 
    plaintext1 = read_file(fn = args.m1).encode()
    plaintext2 = read_file(fn = args.m2).encode()
    plaintext3 = read_file(fn = args.m3).encode()

    #reading the cipher texts
    ciphertext1 = read_bytes(fn = args.c1)
    ciphertext2 = read_bytes(fn = args.c2)
    ciphertext3 = read_bytes(fn = args.c3)

    # The last "length_postfix" bits are chosen at random
    postfix_key = randint(0, 2**length_postfix-1)
    for i in range(2**length_postfix-1):

    #Defining the key for encryption.
     main_key = bin(2 ** 127 + i)
     #write_file(fn = "files/key.bin", value = main_key)
    
    #Encrypting plain-texts.
     nonce1, ctxt1 = encryptor_CTR(message=plaintext1, key=bitstring_to_bytes(main_key))
     #write_bytes(fn = "files/c1.bin", value = ctxt1)
     #write_bytes(fn = "files/nonce1.bin", value = nonce1)    

     nonce2, ctxt2 = encryptor_CTR(message=plaintext2, key=bitstring_to_bytes(main_key))
     #write_bytes(fn = "files/c2.bin", value = ctxt2)
     #write_bytes(fn = "files/nonce2.bin", value = nonce2)    

     nonce3, ctxt3 = encryptor_CTR(message=plaintext3, key=bitstring_to_bytes(main_key))
     #write_bytes(fn = "files/c3.bin", value = ctxt3)
     #write_bytes(fn = "files/nonce3.bin", value = nonce3)    

     #decrypting the cipher texts. 
     pt1=decryptor_CTR(ciphertext1,nonce1,bitstring_to_bytes(main_key))
     pt2=decryptor_CTR(ciphertext2,nonce2,bitstring_to_bytes(main_key))
     pt3=decryptor_CTR(ciphertext3,nonce3,bitstring_to_bytes(main_key))
     if(pt1==plaintext1):
      if((pt2==plaintext2)):
        print("The required key is "+ main_key)
	