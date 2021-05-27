import os
import requests
from bs4 import BeautifulSoup
import redis
from mail_service.mail_service import send_mail


class Scraper:
    def __init__(self, URL, keywords):
        self.URL = URL
        self.keywords = keywords
        self.html = requests.get(self.URL).text
        self.r=redis.from_url(os.environ['REDISCLOUD_URL'])

    def fetch_headlines(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        headlines = soup.findAll("a", {"class": "storylink"})
        self.filtered_headlines  = [headline for headline in headlines if any(keyword.lower() in headline.text.lower() for keyword in self.keywords)]
        # The above LC is same as iterating the headlines and keywords, and appending the headline if keyword is present in headline.

    def store_news(self):
        for headline in self.filtered_headlines:
            self.r.set(headline.text, str(headline))
    
    def mail_news(self):
        news_links = {key.decode("utf-8"): self.r.get(key).decode("utf-8") for key in self.r.keys()}
        if news_links:
            send_mail(news_links)
