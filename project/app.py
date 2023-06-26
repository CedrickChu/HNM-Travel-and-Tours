from flask import Flask, render_template, current_app
from cryptography.fernet import Fernet
from config import Config
import secrets
import requests

app = Flask(__name__)

app.config.from_object('config.Config')

def decrypt_token(encrypted_token, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_token = cipher_suite.decrypt(encrypted_token.encode())
    return decrypted_token.decode()

def inject_nonce():
    return {'nonce': secrets.token_hex(16)}

@app.route("/")
def home():
    encrypted_token = current_app.config['FACEBOOK_ACCESS_TOKEN']
    encryption_key = current_app.config['SECRET_KEY']
    access_token = decrypt_token(encrypted_token, encryption_key)
    latest_post_url = fetch_facebook_posts(access_token)
    return render_template('index.html', latest_post_url=latest_post_url, nonce=inject_nonce())

def fetch_facebook_posts(access_token):
    page_id = '108136152254757'
    limit = 5

    # API request to retrieve the latest posts
    url = f'https://graph.facebook.com/{page_id}/posts?access_token={access_token}&limit={limit}&fields=permalink_url'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_post_url = data['data'][0]['permalink_url']
    else:
        latest_post_url = None

    return latest_post_url

@app.route("/more")
def learnmore():
    return render_template('learnMore.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
