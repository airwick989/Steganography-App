import ast
from AES import AES
from PIL import Image


class AES_Steg:
    def __init__(self, secrets_path):
        self.aes_key = None
        self.aes_iv = None
        self.start_delimiter = None
        self.end_delimiter = None
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
                "start_delimiter": contents[2].strip(),
                "end_delimiter": contents[3].strip()
            }
    
        return secrets
    

    def set_secrets(self, secrets_path):
        secrets = self.get_secrets(secrets_path)
        self.aes_key = secrets['aes_key'].ljust(32, b'\0')  # Pad the key with zeros to make it 32 bytes
        self.aes_iv = secrets['aes_iv']
        self.start_delimiter = secrets['start_delimiter']
        self.end_delimiter = secrets['end_delimiter']


    def encrypt(self, plaintext):
        cipher = self.aes.encrypt(plaintext)
        return cipher
    

    def decrypt(self, cipher):
        plaintext = self.aes.decrypt(cipher)
        return plaintext
    

    def to_bin(self, message):
        binary = ''.join(format(ord(char), '08b') for char in message)
        return binary

    def to_txt(self, binary):
        txt = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return txt


    def embed(self, image_path, plaintext, output_path):
        msg = self.encrypt(plaintext)

        img = Image.open(image_path)
        pixels = list(img.getdata())
        bin_msg = self.to_bin(self.start_delimiter) + self.to_bin(msg) + self.to_bin(self.end_delimiter)

        binary_message_index = 0

        for i in range(len(pixels)):
            pixel = list(pixels[i])
            for j in range(3):  # For RGB channels
                if binary_message_index < len(bin_msg):
                    pixel[j] = pixel[j] & ~1 | int(bin_msg[binary_message_index])
                    binary_message_index += 1

            pixels[i] = tuple(pixel)

        img.putdata(pixels)
        img.save(output_path)


    def extract(self, image_path):
        img = Image.open(image_path)
        pixels = list(img.getdata())

        binary_message = ''

        for i in range(len(pixels)):
            pixel = list(pixels[i])
            for j in range(3):  # For RGB channels
                binary_message += str(pixel[j] & 1)

        start_delimiter = self.to_bin(self.start_delimiter)
        end_delimiter = self.to_bin(self.end_delimiter)

        start_index = binary_message.find(start_delimiter) + len(start_delimiter)
        end_index = binary_message.find(end_delimiter)

        extracted_message = self.to_txt(binary_message[start_index:end_index])
        return extracted_message




plaintext = "Hello there, don't mind if I do! I will certainly eat your croissant :)"
steg = AES_Steg("secrets.txt")
#steg.embed("image.png", plaintext, "encoded_image.png")
extracted = steg.extract('encoded_image.png')
print(f"EXTRACTED: {steg.decrypt(extracted)}")


# encrypted_text = steg.aes.encrypt(plaintext)
# print(f"Encrypted: {encrypted_text}")
# decrypted_text = steg.aes.decrypt(encrypted_text)
# print(f"Decrypted: {decrypted_text}")