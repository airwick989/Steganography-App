from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import ast


class AES:
    def __init__(self, secrets_path):
        self.key = None
        self.iv = None
        self.set_secrets(secrets_path)


    def get_secrets(self, path):
        with open(path, 'r') as file:
            contents = file.readlines()
            secrets = {
                "key": ast.literal_eval(contents[0].strip()),
                "iv": ast.literal_eval(contents[1].strip())
            }
    
        return secrets
    

    #Pad plaintext to meet block size for AES
    def pad(self, data):
        #Initialize padder object
        padder = padding.PKCS7(128).padder()
        #Pad the data, update the padder, and finalize the padded data
        padded_data = padder.update(data) + padder.finalize()
        return padded_data
    

    #Reverses the padding process for decryption
    def unpad(self, data):
        #initialize unpadder object
        unpadder = padding.PKCS7(128).unpadder()
        #unpad the data, update the unpadder, and finalize the unpadded data
        unpadded_data = unpadder.update(data) + unpadder.finalize()
        return unpadded_data
    

    def encrypt(self, plaintext):
        #Produce an AES cipher with CFB mode using the provided key and initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()  #encryptor object

        plaintext = self.pad(plaintext.encode('utf-8'))  #Pad the plaintext
        ciphertext = encryptor.update(plaintext) + encryptor.finalize() #Encrypt the plaintext

        #Combine the ciphertext with the initialization vector, encode it in URL-safe Base64
        return urlsafe_b64encode(self.iv + ciphertext).decode('utf-8')
    

    #Essentially the reverse of the encrypt method
    def decrypt(self, ciphertext):
        data = urlsafe_b64decode(ciphertext.encode('utf-8'))    #Decode ciphertext from URL-safe Base64

        #Extract the ciphertext and initialization vector
        ciphertext = data[16:]
        iv = data[:16]

        #Produce an AES cipher with CFB mode using the provided key and initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()  #decryptor object

        #Decrypt and unpad the ciphertext
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        decrypted_data = self.unpad(decrypted_data)

        #Decode the decrypted data from bytes to UTF-8
        return decrypted_data.decode('utf-8')
    

    def set_secrets(self, secrets_path):
        secrets = self.get_secrets(secrets_path)
        self.key = secrets['key'].ljust(32, b'\0')  # Pad the key with zeros to make it 32 bytes
        self.iv = secrets['iv']
    



# #Example usage
# aes = AES("secrets.txt")
# plaintext = "Hello there, don't mind if I do! I will certainly eat your croissant :)"
# encrypted_text = aes.encrypt(plaintext)
# print(f"Encrypted: {encrypted_text}")
# decrypted_text = aes.decrypt(encrypted_text)
# print(f"Decrypted: {decrypted_text}")