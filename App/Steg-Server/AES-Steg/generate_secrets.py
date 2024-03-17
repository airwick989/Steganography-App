import secrets
import sys
import random
import string

DELIMITER_LENGTH = 6    #Statically assigned delimter length

def generate_aes_key():
    return secrets.token_bytes(32) #generate a random key (32 bytes for AES)

def generate_random_iv():
    return secrets.token_bytes(16)  #generate a random initialization vector (16 bytes for AES)

#Generate random delimters to mark the start and end of encoded messages used in steganography
def generate_random_delimiters(length):
    chars = []
    for i in range(length*2):   #twice the length because 2 delimiters
        chars.append(random.choice(string.ascii_letters + string.digits + string.punctuation))  #Append random ascii character
    #Split the list of characters into start and end delimiters
    start_delimiter = ''.join(chars[:length])
    end_delimiter = ''.join(chars[length:])
    return (start_delimiter, end_delimiter)



def generate_secrets(path):
    #Write contents to secrets file
    with open(path, "w+") as file:
        file.write(f"{str(generate_aes_key())}\n")
        file.write(f"{str(generate_random_iv())}\n")

        delimiters = generate_random_delimiters(DELIMITER_LENGTH)
        file.write(f"{delimiters[0]}\n")
        file.write(delimiters[1])