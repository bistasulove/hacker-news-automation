import os
import requests
from bs4 import BeautifulSoup
import redis
from mail_service.mail_service import send_mail
import json



class Scraper:
    def __init__(self, email, URL, keywords):
        self.URL = URL
        self.email = email
        self.keywords = keywords
        self.html = requests.get(self.URL).text
        self.r=redis.from_url(os.environ['REDISCLOUD_URL'])

    def fetch_headlines(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        headlines = soup.findAll("a", {"class": "storylink"})
        self.filtered_headlines  = [headline for headline in headlines if any(keyword.lower() in headline.text.lower() for keyword in self.keywords)]
        # The above LC is same as iterating the headlines and keywords, and appending the headline if keyword is present in headline.
        print("Filtered Headlines:", self.filtered_headlines)
        

    def store_news(self):
        news = {headline.text: str(headline) for headline in self.filtered_headlines}
        if self.r.get(self.email):
            print("Found existing email")
            old_data = json.loads(self.r.get(self.email).decode('utf-8'))
            news.update(old_data)
        self.r.set(self.email, json.dumps(news))

        print("This is saved till now in redis: ", self.r.get(self.email))
    
    def mail_news(self):
        news = json.loads(self.r.get(self.email).decode('utf-8'))
        news_links = list(news.values())
        print(f"For email {self.email}: found {len(news_links)} news")
        if news_links:
            send_mail(self.email, news_links)
            self.r.delete(self.email)