# Password Manager
# 23/11/2019
# Program created by - Subramanya Soujanya Akella and Meghana Reddy Akkati
#
# This program stores passwords in a file that is encrypted with a master password. 
# Passwords can be retrieved by providing the website name.
#
# references:
#   1. https://stackoverflow.com/questions/19232011/convert-dictionary-to-bytes-and-back-again-python

import os
from sys import argv
import bcrypt
import pyAesCrypt as pyAESCrypt
import json
import random
import string

PASSWORD_FILE_PATH = "pwManDataBase"
ENCRYPT_BUFF_SIZE = 64 * 1024
SALT = b'$2b$12$l/Jycm9Th2UrINV9zpr6l.'  # this is our salt that we will hash with the master password to prevent brute forcing

# reference 1
def dictToBytes(dict):
	return json.dumps(dict).encode()
def bytesToDict(dict):
	return json.loads(dict.decode())


def setDB(passwordDB, key):
    with open(PASSWORD_FILE_PATH, "wb") as passwordFile:  # mode 'w' will overwrite whatever is already in the file
        passwordFile.write(dictToBytes(passwordDB))  # overwrite existing database with new one (unencrypted)
    pyAESCrypt.encryptFile(PASSWORD_FILE_PATH, PASSWORD_FILE_PATH+".temp", key.decode(), ENCRYPT_BUFF_SIZE)  # encrypt it to a temp file
    os.replace(PASSWORD_FILE_PATH+".temp", PASSWORD_FILE_PATH)

    

def getDB(key):
    if not os.path.isfile(PASSWORD_FILE_PATH):  # doesn't already exist
        print("No password database, creating...")
        setDB({}, key)
        return {}  # it doesn't exist, so just return an empty dict
    
    pyAESCrypt.decryptFile(PASSWORD_FILE_PATH, PASSWORD_FILE_PATH+".temp", key.decode(), ENCRYPT_BUFF_SIZE)  # create a file with .temp extension that's decrypted
    
    with open(PASSWORD_FILE_PATH+".temp", "rb") as passwordFile:
        ret = bytesToDict(passwordFile.read())
    os.remove(PASSWORD_FILE_PATH+".temp")  # remove decrypted database file
    return ret


def main():
    if len(argv) != 2:  # 2 is correct number of arguments
        print("usage: python pwMan.py <website>")  # inform the user on correct script usage
        return  # exit the script

    masterpw = input("Enter Master Password: ")
    key = bcrypt.hashpw(masterpw.encode(), SALT)  # we use bcrypt to combine the master password with the salt to prevent brute forcing

    print("Loading database...")
    try:
     passwordDB = getDB(key)
    except ValueError:  # the password is incorrect (most likely) or the password file is corrupt (less likely)
        print("Wrong password or password file corrupted")
        return

    entry = argv[1]
    if entry in passwordDB:
        print(f"entry   : {entry}")
        print(f"password: {passwordDB[entry]}")
    else:
        print(f"No entry for {entry}, creating new...")
        newPass = input(f"New entry - enter password for {entry} (leave blank for automatic generation): ")
        if newPass == "":
            newPass = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
            print(f"Randomly generated password is {newPass}")
        passwordDB[entry] = newPass
        setDB(passwordDB, key)
        print("stored")
    
    

if __name__ == "__main__":
    main()