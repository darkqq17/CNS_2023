output = 'Oh gOod! i wAs just thinKING that The siLk FlOwerS aT ThE FeiyUn commeRCe gUild NeeDed waTerinG. THe tRanSpoRT CoorDiNAtoRs wILL ProbAbLy MoAn abouT THe muddy mOUNtaIn roADS agaIN, tHouGH...'

lookup = {
    'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
    'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
    'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
    'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
    'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab'
}

decipher = ""
for letter in output:
    if letter.isupper() == True:
        decipher += "b"
    elif letter.islower() == True:
        decipher += "a"
print(decipher)

result = ""
i = 0
while True:
    # condition to run decryption till
    # the last set of ciphertext
    if(i < len(decipher)-4):
        # extracting a set of ciphertext
        # from the message
        substr = decipher[i:i + 5]
        # checking for space as the first
        # character of the substring
        if(substr[0] != ' '):
            '''
            This statement gets us the key(plaintext) using the values(ciphertext)
            Just the reverse of what we were doing in encrypt function
            '''
            result += list(lookup.keys())[list(lookup.values()).index(substr)]
            i += 5  # to get the next set of ciphertext

        else:
            # adds space
            result += ' '
            i += 1  # index next to the space
    else:
        break  # emulating a do-while loop
print(result)