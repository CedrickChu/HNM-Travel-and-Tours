from flask import Flask, render_template, current_app, jsonify

import os
import secrets
import requests
from datetime import datetime, timedelta



app = Flask(__name__)

gallery = [
        {
            
            'id': 'Attraction1',
            'class=' : 'mySlides1',
            'heading': "1.) Underground River Tour",
            'description': "Puerto Princesa City is the center of Palawan and best known for the internationally recognized Puerto Princesa Subterranean River (or Underground River), a UNESCO World Heritage Site and one of the New 7 Wonders of Nature. Not only that, the city is critically acclaimed for its environmental excellence.",
            'image': ["/static/images/underground.jpg", "/static/images/underground2.jpg", "/static/images/underground3.jpg"]
        },
        {
           
            'id': 'Attraction2',
            'class=' : 'mySlides2',
            'heading': "2.) El Nido Island Hopping",
            'description': "El Nido, located on Palawan island in the Philippines, is recognized for its pristine beaches and vibrant coral reefs. Despite the 5-6 hour drive from the town center, the journey is worthwhile due to the island's abundant natural beauty and awaiting ecosystem.",
            'image': ["/static/images/elnido.jpg", "/static/images/elnido-beach.jpg", "/static/images/elnidoBeach.jpg"]
        },
        {
            
            'id': 'Attraction3',
            'class=' : 'mySlides3',
            'heading': "3.) Culion Island Hopping",
            'description': "Culion Island, situated in the northern part of Palawan, Philippines, is a captivating destination with a rich historical significance and natural charm. It is part of the Calamianes Group of Islands and is known for its tranquil atmosphere and stunning landscapes. Culion Island is also known for its vibrant marine life and coral reefs. Snorkelers and divers can explore the underwater world, discovering colorful coral formations and an array of tropical fish species. The island's waters are teeming with marine biodiversity, offering a memorable experience for those seeking to immerse themselves in its underwater wonders.",
            'image': ["/static/images/culionIsland2.jpg", "/static/images/culionIsland.jpg", "/static/images/Culion-Island.jpg"]
        },
        {
            
            'id': 'Attraction4',
            'class=' : 'mySlides4',
            'heading': "4.) Honda Bay Island Escape",
            'description': "Puerto Princesa’s Honda Bay is blessed with white sand beaches and small islands rich in marine life, and you can visit the top attractions all in just one day with Honda Bay island-hopping adventures.",
            'image': ["/static/images/hondaBay.jpg", "/static/images/hondaBay2.jpg", "/static/images/hondaBay3.jpg"]
        },
         {
            
            'id': 'Attraction5',
            'class=' : 'mySlides5',
            'heading': "5.) Balabac Island Hopping",
            'description': "Balabac Island is a captivating gem located in the southernmost part of Palawan, Philippines. It is part of the Calamianes Group of Islands and boasts a mesmerizing combination of natural wonders and pristine beauty.The island is renowned for its remarkable biodiversity and is home to numerous species of flora and fauna. With its lush forests and untouched wilderness, Balabac Island offers a unique opportunity for nature enthusiasts and adventurers to immerse themselves in its breathtaking landscapes.",
            'image': ["/static/images/mansalanganbalabac.png", "/static/images/balabac3.png", "/static/images/balabac2.jpg"]
        },
         {
            
            'id': 'Attraction6',
            'class=' : 'mySlides6',
            'heading': "6.) coron island hopping",
            'description': "Coron is part of the Calamianes Group of Islands and located on the northern tip of Palawan. It has seven lakes, famous of which is the nationally-acclaimed cleanest lake in the Philippines, the Kayangan Lake. It also has a number of islands with white beaches and clear blue waters perfect for snorkeling, deep sea fishing, and shipwreck diving.",
            'image': ["/static/images/kayanganLake.jpg", "/static/images/kayanganLake2.jpg", "/static/images/coron2.jpg"]
        },
    ]

def inject_nonce():
    return {'nonce': secrets.token_hex(16)}


@app.route("/")
def home():
    
    access_token = ("FACEBOOK_ACCESS_TOKEN")
    latest_post_urls = fetch_facebook_posts(access_token)
    return render_template('index.html', latest_post_urls=latest_post_urls, gallery=gallery,nonce=inject_nonce())



def fetch_facebook_posts(access_token, hashtag='#TicketsOnSale', days=30):
    page_id = "108136152254757"
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

@app.route("/api/gallery")
def carousel():
    return jsonify(gallery)

@app.route("/test")
def test():
    return render_template('test.html', gallery=gallery)

@app.route("/more")
def learnmore():
  return render_template('learnMore.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


