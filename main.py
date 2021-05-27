from flask import Flask
from scrape_service.scrape import Scraper
app = Flask(__name__)

@app.route('/')
def index():
    s = Scraper('https://news.ycombinator.com/', ['microsoft'])
    s.fetch_headlines()
    s.store_news()
    s.mail_news()
    return "Successfully sent"