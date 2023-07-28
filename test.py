from Crypto.Cipher import AES
import binascii
import secret

def pad(m):
    length = 16-len(m) % 16
    return m+chr(length).encode()*length

def encrypt(m):
    aes = AES.new(secret.key, AES.MODE_CBC, secret.iv)
    return binascii.hexlify(aes.encrypt(pad(m))).decode()
test = "70309f98653e87df804263d5a0348f115c36bc7c2cddfe02ffd44528083635404815ed8c0f14ad8cbbb1c7bc12bf21725fa15c0e7ba326e433ec41ddfaf41d27aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04fbe"
text = "70309f98653e87df804263d5a0348f115c36bc7c2cddfe02ffd44528083635404815ed8c0f14ad8cbbb1c7bc12bf21725fa15c0e7ba326e433ec41ddfaf41d27aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04fbe"
text_4 = "aa18ce4381a61d187ecbdcc974074701 00b7f354bb68139f2306508a06a04fbe"
test_4 = "aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04f"
print(len(text_4))
