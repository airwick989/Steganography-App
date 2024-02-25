import secrets
import sys
import random
import string

DELIMITER_LENGTH = 6

def generate_aes_key():
    return secrets.token_bytes(32) #generate a random key (32 bytes for AES)

def generate_random_iv():
    return secrets.token_bytes(16)  #generate a random initialization vector (16 bytes for AES)

def generate_random_delimiters(length):
    chars = []
    for i in range(length*2):
        chars.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
    start_delimiter = ''.join(chars[:length])
    end_delimiter = ''.join(chars[length:])
    return (start_delimiter, end_delimiter)


if len(sys.argv) == 1:
    PATH = "secrets.txt"
else:
    PATH = str(sys.argv[1])
with open(PATH, "w+") as file:
    file.write(f"{str(generate_aes_key())}\n")
    file.write(f"{str(generate_random_iv())}\n")

    delimiters = generate_random_delimiters(DELIMITER_LENGTH)
    file.write(f"{delimiters[0]}\n")
    file.write(delimiters[1])