from pwn import *

def padding(text):
    output = ""
    text.recvuntil("ID: ")
    output_1 = text.recvline().decode()
    output += output_1[:-3]
    text.recvuntil("| ")
    output_2 = text.recvline().decode()
    output += output_2[:-3]
    text.recvuntil("| ")
    output_3 = text.recvline().decode()
    output += output_3[:-3]
    text.recvuntil("| ")
    output_4 = text.recvline().decode()
    output += output_4[:-3]
    
    text.sendlineafter("Your choice: ", "2")
    text.sendlineafter("Your choice: ", "1")

    quit = 0
    if quit == 1:
        text.sendlineafter("Please give me the ID (hex encoded): ", test_cache)
    a, b = output[-64:-34], output[-32:]
    for x in range(0, 10):
        cache_1 = f"{x}"
        for y in range(0, 10):
            cache_2 = f"{y}"
            test_cache = a + cache_1 + cache_2 + b
            if quit == 0:
                quit += 1
                text.sendlineafter("Please give me the ID (hex encoded): ", test_cache)
                

    

if __name__ == "__main__":
    context.encoding = "utf-8"
    context = remote('cns.csie.org', 44399)
    padding(context)
    context.interactive()