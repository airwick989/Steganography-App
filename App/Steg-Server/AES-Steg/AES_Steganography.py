import ast
from AES import AES
from PIL import Image


class AES_Steg:
    def __init__(self, secrets_path):
        self.aes_key = None
        self.aes_iv = None
        self.start_delimiter = None
        self.end_delimiter = None
        self.set_secrets(secrets_path)  #obtain secrets from secrets file
        aes_secrets = {
            "key": self.aes_key,
            "iv": self.aes_iv
        }
        self.aes = AES(secrets=aes_secrets) #set sercrets specific to AES and instantiate AES object


    #Obtain secrets from secrets file
    def get_secrets(self, path):
        with open(path, 'r') as file:
            #Extract each secret line-by-line
            contents = file.readlines()
            secrets = {
                "aes_key": ast.literal_eval(contents[0].strip()),
                "aes_iv": ast.literal_eval(contents[1].strip()),
                "start_delimiter": contents[2].strip(),
                "end_delimiter": contents[3].strip()
            }
    
        return secrets
    

    #Set all secrets used for both AES and steganography from the secrets file
    def set_secrets(self, secrets_path):
        secrets = self.get_secrets(secrets_path)
        self.aes_key = secrets['aes_key'].ljust(32, b'\0')  # Pad the key with zeros to make it 32 bytes
        self.aes_iv = secrets['aes_iv']
        self.start_delimiter = secrets['start_delimiter']
        self.end_delimiter = secrets['end_delimiter']


    #Encrypt the plaintext using AES encryption
    def encrypt(self, plaintext):
        cipher = self.aes.encrypt(plaintext)
        return cipher
    

    #Decrypt the plaintext using AES decryption
    def decrypt(self, cipher):
        plaintext = self.aes.decrypt(cipher)
        return plaintext
    

    #Convert text to binary (convert each character into its 8-bit representation)
    def to_bin(self, message):
        binary = ''.join(format(ord(char), '08b') for char in message)
        return binary

    #Convert binary to text
    def to_txt(self, binary):
        txt = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return txt


    #Embed message into image using LSB steganography
    def embed(self, image_path, plaintext, output_path):
        msg = self.encrypt(plaintext)   #Encrypt message using AES

        img = Image.open(image_path)    #Open image for pillow processing 
        img_data = list(img.getdata())  #Retrieve pixel values from image, each pixel holds a RGB tuple
        #converg encrypted message to binary, convert delimiters to binary, add them to the message
        bin_msg = self.to_bin(self.start_delimiter) + self.to_bin(msg) + self.to_bin(self.end_delimiter)

        #Check if image is large enough to embed the binary message
        if len(bin_msg) > len(img_data)*3:
            raise ValueError("Message is too large to be embedded in the image. Please choose a larger image or a smaller message.")

        bin_msg_index = 0   #Keep track of index in binary message   
        for i in range(len(img_data)):  #Iterate through each pixel
            pixel = list(img_data[i])   #Divide pixel into RGB values
            for j in range(3):  #For each RGB channel, do the following
                if bin_msg_index < len(bin_msg):    #Check if binary message has been iterated through
                    """
                    For each RGB channel, clear (set to 0) the LSB of current channel using a bitwise operation 
                    (~1 creates a bitmask with all bits set to 1 except the LSB, and & operation with current pixel values clears the LSB)
                    Then the next bit from binary message will replace the cleared LSB using an OR (|) bitwise operation
                    """
                    pixel[j] = pixel[j] & ~1 | int(bin_msg[bin_msg_index])
                    bin_msg_index += 1  #Move to next bit in binary message

            img_data[i] = tuple(pixel)  #Set pixel value to new tuple

        img.putdata(img_data)   #Set new image data with updated pixel values
        img.save(output_path)   #Save image with embedded data


    #Extract message from encoded image
    def extract(self, image_path):
        #Open image and extract pixel values 
        img = Image.open(image_path)
        img_data = list(img.getdata())

        bin_msg = ''    #Container for binary message
        for i in range(len(img_data)):  #Iterate through each opixel
            pixel = list(img_data[i])   #Divide pixel into RGB channels
            for j in range(3):  # For each RGB channel, do the following
                bin_msg += str(pixel[j] & 1)    #Retrieve the LSB by using bitwise & operation with 1 (0001), append to binary message

        #Geg binary delimiters
        start_delimiter = self.to_bin(self.start_delimiter)
        end_delimiter = self.to_bin(self.end_delimiter)

        start_index = bin_msg.find(start_delimiter) + len(start_delimiter)  #Get index where message begins
        end_index = bin_msg.find(end_delimiter) #Get index where message ends

        #Obtain message using start and end indeces
        extracted_msg = self.to_txt(bin_msg[start_index:end_index]) #Convert binary message to text
        return self.decrypt(extracted_msg)  #Use AES decryption to decrypt the text




# #Example usage
# plaintext = "Hello there, don't mind if I do! I will certainly eat your croissant :)"
# steg = AES_Steg("secrets.txt")
# steg.embed("image.png", plaintext, "encoded_image.png")
# print(f"EXTRACTED: {steg.extract('encoded_image.png')}")