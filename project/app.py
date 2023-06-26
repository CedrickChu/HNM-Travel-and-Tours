from flask import Flask, render_template, current_app
import os
import secrets
import requests
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
def inject_nonce():
    return {'nonce': secrets.token_hex(16)}

@app.route("/")
def home():
    access_token = os.environ['FACEBOOK_ACCESS_TOKEN']
    print(f"Access token: {{access_token}}")
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