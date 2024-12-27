import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

encrypt_keys = ['chp5+E2AI5H/IZAh+CZcgvfWD8LT5xx5pNw4EBzvSW4=', 'XeY25bdnBxxNRUxh4WojnXHAl2AZZeE/ZCRaZ8tilBg=',
                'T4HebrPNZM9iUxWw9S4eabKxTt/e5IpmTFRdYKP0P6M=', 'UwbH4iQckGFwLcJxb7bTl7WZ1Ck7AQnmU7j+3Pnn8qg=',
                'Ybdqtx7bBZRIsTHcGIYjfmmJsF/noBRsqQvdOhDjiks=', '7w/PFIIlq7rGYsdmvpXFIctWWv/aTJ6wFM5Abk4ICBM=',
                'ME3W0Tnv99WmbxCzksiCWGcot7hFppJAdhYFgzpdaK8=', 'JEzpI59c5LGtOV/O169viLAU2pbwilK6fcVnQPUSlNw=',
                'Bx+1wX+5LELTMnDWFHXGR6g3SX4DB/i/hKLYzP/6Ph0=', '6aUlPv2qzppSY55r5n3vVkLOlUrX25+NPXxLR62zO54=',
                'tc/W8ZY1/aXP7YBowpvgNFd0SjKhNAeFoDw2Lwrnazc=', 'wPln2yFTxebb+vvpyo0B1HxH6rC7rviusNI+OMTy1sk=',
                '3CIPhS4gbJmR8r+SW+9Tjol474C+77ORcac3cD3pwWI=', 'mrSmeh5rrxIdrSTs+hblqsHWgduKNDX4KjKGh5I+ivE=',
                '+cRetN71+ona6wk55H+gMOlT/8OFFRWQaDTZZ0nDnAw=', 'eFRWpzMiDmm2m7u0J8kAfrC01jUn5Po422sAatfrHig=']

access_key = 'JMOOciL7zeMZIRS0'
image_code = 'YtRCMnnWWU4xFO3z3Iufa8nGq7UyOQ4lSwIk6LDGz9aZCtlb6lOZZwUQq2L6YGDiwRx6qfPT2THG2UlRYAVVUzYibKZCWV8L0ZTo4dmVX2xUbA6Sk2mQtdOBuHBsos5Sa6xkNIhvlpmv2WkiKluzIg=='

# 选择密钥
key1 = encrypt_keys[ord(access_key[-1]) % len(encrypt_keys)]
key2 = encrypt_keys[ord(access_key[0]) % len(encrypt_keys)]

# 第一轮解密
cipher = base64.b64decode(image_code)
iv = cipher[:16]
cipher_text = pad(cipher[16:], AES.block_size, style='ZERO')
cipher = AES.new(base64.b64decode(key1), AES.MODE_CBC, iv).decrypt(cipher_text)
cipher = base64.b64encode(cipher).decode('utf-8')

# 第二轮解密
cipher = base64.b64decode(cipher)
iv = cipher[:16]
cipher_text = pad(cipher[16:], AES.block_size, style='ZERO')
plaintext = AES.new(base64.b64decode(key2), AES.MODE_CBC, iv).decrypt(cipher_text)

print(unpad(plaintext, AES.block_size, style='ZERO').decode('utf-8'))