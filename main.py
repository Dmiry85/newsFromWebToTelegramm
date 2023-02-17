from models import *
import asyncio

rbk = NewsRbk()
bot = MyBot()


async def main():
    if __name__ == '__main__':
        while True:
            task1 = bot.news_every_minute(rbk.get_articles())
            await task1
            await asyncio.sleep(30)

asyncio.run(main())
