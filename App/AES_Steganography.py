import ast
from AES import AES
from PIL import Image


class AES_Steg:
    def __init__(self, secrets_path):
        self.aes_key = None
        self.aes_iv = None
        self.delimiter = None
        self.set_secrets(secrets_path)
        aes_secrets = {
            "key": self.aes_key,
            "iv": self.aes_iv
        }
        self.aes = AES(secrets=aes_secrets)


    def get_secrets(self, path):
        with open(path, 'r') as file:
            contents = file.readlines()
            secrets = {
                "aes_key": ast.literal_eval(contents[0].strip()),
                "aes_iv": ast.literal_eval(contents[1].strip()),
                "secret_delimiter": contents[2].strip()
            }
    
        return secrets
    

    def set_secrets(self, secrets_path):
        secrets = self.get_secrets(secrets_path)
        self.aes_key = secrets['aes_key'].ljust(32, b'\0')  # Pad the key with zeros to make it 32 bytes
        self.aes_iv = secrets['aes_iv']
        self.delimiter = secrets['secret_delimiter']


    def encrypt(self, plaintext):
        cipher = self.aes.encrypt(plaintext)
        return cipher
    

    def decrypt(self, cipher):
        plaintext = self.aes.encrypt(cipher)
        return plaintext


    pass




# plaintext = "Hello there, don't mind if I do! I will certainly eat your croissant :)"
steg = AES_Steg("secrets.txt")
# print(steg.encrypt(plaintext))
# steg.embed("image.png", plaintext, "encoded_image.png")
steg.extract("encoded_image.png")


# encrypted_text = steg.aes.encrypt(plaintext)
# print(f"Encrypted: {encrypted_text}")
# decrypted_text = steg.aes.decrypt(encrypted_text)
# print(f"Decrypted: {decrypted_text}")