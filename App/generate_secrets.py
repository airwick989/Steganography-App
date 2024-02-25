import secrets
import sys
import random
import string

DELIMITER_LENGTH = 6

def generate_aes_key():
    return secrets.token_bytes(32) #generate a random key (32 bytes for AES)

def generate_random_iv():
    return secrets.token_bytes(16)  #generate a random initialization vector (16 bytes for AES)

def generate_random_delimiter(length):
    chars = []
    for i in range(length):
        chars.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
    return ''.join(chars)


if len(sys.argv) == 1:
    PATH = "secrets.txt"
else:
    PATH = str(sys.argv[1])
with open(PATH, "w+") as file:
    file.write(f"{str(generate_aes_key())}\n")
    file.write(f"{str(generate_random_iv())}\n")
    file.write(generate_random_delimiter(DELIMITER_LENGTH))