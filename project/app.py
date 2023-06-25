from flask import Flask, render_template, request, current_app
import os
import secrets
import requests
import time


app = Flask(__name__)
app.config.from_object('config.Config')

os.environ['FACEBOOK_ACCESS_TOKEN'] = 'EAABy1Nh5yhwBABtiPCwzsM5pzNbuQ9i5GaGYu9fJhKVWiC7gJAo03XdtB3Gm1WlFuaSm7ALMMjU3c0zMclIoCJMMUokArE3pulp9sOo2XFc7OarHd9wfAxvVl51dbi771ntngzQeFEHoXlAPdFyEi9xWIIPcagLxCBO2h2c9ajQKckiYkh8aFOHjb51BfxKnq1t9azeWbkZBaZCZBAl'

def inject_nonce():
    return {'nonce': secrets.token_hex(16)}

@app.route("/")

def home():
    latest_post_url = fetch_facebook_posts()
    return render_template('index.html', latest_post_url=latest_post_url, nonce=inject_nonce())

def fetch_facebook_posts():
    page_id = '108136152254757'
    access_token = current_app.config['FACEBOOK_ACCESS_TOKEN']
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
