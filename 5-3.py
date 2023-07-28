import base64

output = 'v8vUdl0EeZroB/ZdxkEJSr67bp15KsAz8nsdYkeXqFGPiQk4NItADw=='
encoded_data = base64.b64encode(output[1:-2])
print(encoded_data)