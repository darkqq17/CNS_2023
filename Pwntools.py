from pwn import *
r = remote('cns.csie.org', 44398)
r.recvuntil('[?] ') # readline
txt = r.recvline()
print(txt)
r.sendlineafter('>>>', '10') # 在前面那個參數後再發送訊息
r.interactive()
