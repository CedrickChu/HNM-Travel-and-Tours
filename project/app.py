from flask import Flask, render_template, current_app
import os
import secrets
import requests
import logging
from datetime import datetime, timedelta

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def inject_nonce():
    return {'nonce': secrets.token_hex(16)}

@app.route("/")
def home():
    access_token = ['FACEBOOK_ACCESS_TOKEN']
    latest_post_urls = fetch_facebook_posts(access_token)
    return render_template('index.html', latest_post_urls=latest_post_urls, nonce=inject_nonce())


def fetch_facebook_posts(access_token, hashtag='#TicketsOnSale', days=30):
    page_id = '108136152254757'
    limit = 5

    # Calculate the date range for fetching posts
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # API request to retrieve the posts within the date range
    url = f'https://graph.facebook.com/{page_id}/posts?access_token={access_token}&limit={limit}&fields=permalink_url,message,created_time'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            posts = data['data']
            latest_posts = []
            for post in posts:
                message = post.get('message', '')
                created_time = post.get('created_time')
                post_date = datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S+0000")
                if start_date <= post_date <= end_date and hashtag in message:
                    post_data = {
                        'permalink_url': post['permalink_url'],
                        'created_time': post_date
                    }
                    latest_posts.append(post_data)
            latest_posts = sorted(latest_posts, key=lambda x: x['created_time'], reverse=True)
            latest_post_urls = [post['permalink_url'] for post in latest_posts]
        else:
            latest_post_urls = []
    else:
        latest_post_urls = []

    return latest_post_urls[:limit]



@app.route("/more")
def learnmore():
  return render_template('learnMore.html')

@app.route("/test")
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


