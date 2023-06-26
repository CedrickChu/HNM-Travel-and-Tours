from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt the access token
access_token = "EAABy1Nh5yhwBAAya015uFR7HZBTNiZA8RcZBhxtt1PZAzj8jrZCsLErVEPwIIkLTmEZBN6buEvKKzJuRhvgZBAuXn6d1TuFOHPGKQioL78drZAoC34QB2zV15GFCLQAkmMLaZAksuoiSQZBzjO1xeDZBTC6TRL0WAHrvBXPR5vNL9jMXVSAl8T5JuZBGor8ba2LTxexdPlZAhpoOeTgv5kfg45aNdNUrbn6AF9ogZD"
encrypted_token = cipher_suite.encrypt(access_token.encode())

class Config:
    FACEBOOK_ACCESS_TOKEN = encrypted_token.decode()
    SECRET_KEY = key.decode()
