import requests
from bs4 import BeautifulSoup
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hlink
from config import token, user1_id, user2_id


# Class to get news from RBK website
class NewsRbk:
    def __init__(self, keywords="All"):
        self.url = "https://www.rbc.ua/ukr/news"
        # Set User-Agent header to avoid getting blocked by website
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
        }
        self.last_article_id = None
        self.keywords = keywords
    
    # Function to get articles from RBK website
    def get_articles(self):
        r = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        articles = soup.find(class_="newsline").find_all("a")
        news_dict = {}
        for item in articles:
            # Check if article has time info
            if item.find(class_="time"):
                article_time = item.find(class_="time").text.strip()
                article_title = item.get_text()
                article_title = article_title.strip()
                article_title = article_title.replace("\n", " ")
                article_url = item.get('href')
                article_id = article_url.split("/")[-1]
                article_id = article_id[-15:-5]
                # Add new article to dictionary if its id is not equal to the last article id
                if article_id != self.last_article_id:
                    news_dict[article_id] = {
                        "article_time": article_time,
                        "article_title": article_title,
                        "article_url": article_url,
                    }
                else:
                    break
        # If there are any new articles, update the last_article_id and write the dictionary to a file
        if list(news_dict.keys()):
            self.last_article_id = (list(news_dict.keys())[0])
        with open("news_dict.json", "w") as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)

        return news_dict


# Class to initialize bot and send news to users
class MyBot:
    def __init__(self):
        self.bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot)

    # Coroutine to send news to users
    async def news_every_minute(self, func):
        fresh_news = func
        # Check if there are any fresh news
        if len(fresh_news) >= 1:
            fresh_news = dict(reversed(list(fresh_news.items())))
            for k, v in fresh_news.items():
            # Create message with article title and url
                news = f"{hlink(v['article_title'], v['article_url'])}"
                print(news)
                # Send message to users with the news and disable notifications
                await self.bot.send_message(user1_id, news, disable_notification=True)
                await self.bot.send_message(user2_id, news, disable_notification=True)
        # else:
            # await self.bot.send_message(user_id, "There are no fresh news ...", disable_notification=True)
            # print("There are no fresh news ...")
