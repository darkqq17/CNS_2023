from pwn import *

def decrypt_caesar_cipher(text, shift):
    decrypted_text = ""

    for char in text:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted < ord("a"):
                    shifted += 26
            elif char.isupper():
                if shifted < ord("A"):
                    shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char

    return decrypted_text

def try_all_shifts(text):
    for shift in range(1, 27):
        decrypted_text = decrypt_caesar_cipher(text, shift)
        log.info(f"Shift: {shift}, Decrypted text: {decrypted_text}")

# Example usage:
cipher_text = "vkxyut igt ktixevz g yesskzxoi qke ubkx"
try_all_shifts(cipher_text)