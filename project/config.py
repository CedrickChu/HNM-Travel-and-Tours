from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt the access token
access_token = "EAABy1Nh5yhwBAIpdmlAtbHK7V0mU1gKShjG7XaTcTWoXYNUjpATKek2cbtdQQrreBFSbOPCEGiLfsznQlW4CIsSvaic2HfxXw8SzCRmZC2gCa6vUEZAX8gdQv4Ks38SNow5oN3gpLrKcIHDs38o6oi1tmZBYfREcqpuaW11isczvwfTTZA8c9tGm4o12ivUZB9bCOc2faebdzrwFjNBStFDrcn1vf814ZD"
encrypted_token = cipher_suite.encrypt(access_token.encode())

class Config:
    FACEBOOK_ACCESS_TOKEN = encrypted_token.decode()
    SECRET_KEY = key.decode()
