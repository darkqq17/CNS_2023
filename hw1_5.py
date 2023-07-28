from pwn import *
import base64

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

# ref: https://www.geeksforgeeks.org/rail-fence-cipher-encryption-decryption/
def decryptRailFence(cipher, key):

    rail = [['\n' for i in range(len(cipher))]
                for j in range(key)]
    # to find the direction
    dir_down = None
    row, col = 0, 0
     
    # mark the places with '*'
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
         
        # place the marker
        rail[row][col] = '*'
        col += 1
         
        # find the next row
        # using direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
             
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if ((rail[i][j] == '*') and
            (index < len(cipher))):
                rail[i][j] = cipher[index]
                index += 1
         
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
         
        # check the direction of flow
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False
             
        # place the marker
        if (rail[row][col] != '*'):
            result.append(rail[row][col])
            col += 1
             
        if dir_down:
            row += 1
        else:
            row -= 1
    return("".join(result))

#ref :https://www.geeksforgeeks.org/baconian-cipher/
def Baconian(text):
    text.recvuntil('c = ')
    output = text.recvline().decode()[1:-2]

    lookup = {
        'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
        'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
        'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
        'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
        'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 
        'Z': 'bbaab'
    }

    decipher = ""
    for letter in output:
        if letter.isupper() == True:
            decipher += "b"
        elif letter.islower() == True:
            decipher += "a"
    
    result = ""
    i = 0
 
    while True:
        if(i < len(decipher)-4):
            substr = decipher[i:i + 5]

            if(substr[0] != ' '):
                result += list(lookup.keys())[list(lookup.values()).index(substr)]
                i += 5  # to get the next set of ciphertext
            else:
                # adds space
                result += ' '
                i += 1 
        else:
            break 

    for key in range(2, len(result)):
        answer = decryptRailFence(result, key)
        log.info(f"Shift: {key}, Decrypted text: {answer}")
    key = int(input("select key: "))
    answer = decrypt_caesar_cipher(result, key).lstrip("\'").rstrip("\'\n")

    text.sendlineafter(">>> ", answer)

def Question0(text):
    text.recvuntil('[?] ')
    output = text.recvline().decode()
    result = str(eval(output.split("=")[0]))
    text.sendlineafter(">>> ", result)

    text.recvuntil('! ')
    output = text.recvline().decode()
    output = output.split("\"")[1]
    text.sendlineafter('>>>', output)

def caesar(text):
    text.recvuntil('c = ')
    output = text.recvline().decode()
    for shift in range(1, 27):
        decrypted_text = decrypt_caesar_cipher(output, shift)
        log.info(f"Shift: {shift}, Decrypted text: {decrypted_text}")
    
    key = int(input("select key: "))
    result = decrypt_caesar_cipher(output, key).lstrip("\'").rstrip("\'\n")

    text.sendlineafter(">>> ", result)

def railfence(text):
    text.recvuntil('c = ')
    output = text.recvline().decode()[1:-2]
    for key in range(2, len(output)):
        result = decryptRailFence(output, key)
        log.info(f"Shift: {key}, Decrypted text: {result}")

    key = int(input("select key: "))   
    result = decryptRailFence(output, key).lstrip("\'").rstrip("\'\n")

    text.sendlineafter(">>> ", result)

def onetimepad(text):
    text.recvuntil('(c1) = ')
    c1 = text.recvline().decode()[2:-2]
    text.recvuntil('m1 = ')
    m1 = text.recvline().decode()[1:-2]
    text.recvuntil('(c2) = ')
    c2 = text.recvline().decode()[2:-2]

    encoded_data_1 = base64.b64decode(c1)
    encoded_data_2 = base64.b64decode(c2)
    
    result = ""
    for a, b, c in zip(encoded_data_1, m1, encoded_data_2):
        answer = a^ord(b)^c
        result += chr(answer)

    result = result.lstrip("\'").rstrip("\'\n")
    text.sendlineafter(">>> ", result)

def flag(text):
    text.recvuntil('flag: ')
    output = text.recvline().decode()
    output = base64.b64decode(output)
    text.sendlineafter(">>> ", output)

if __name__ == "__main__":
    context.encoding = "utf-8"
    context = remote('cns.csie.org', 44398)
    Question0(context)
    caesar(context)
    railfence(context)
    onetimepad(context)
    Baconian(context)
    flag(context)
    context.interactive()
