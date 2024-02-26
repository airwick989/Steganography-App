from AES_Steganography import AES_Steg

plaintext = "Hello there, don't mind if I do! I will certainly eat your croissant :)"
steg = AES_Steg("secrets.txt")
steg.embed("image.png", plaintext, "encoded_image.png")
print(f"EXTRACTED: {steg.extract('encoded_image.png')}")