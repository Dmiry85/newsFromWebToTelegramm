from models import *
import asyncio

# Create instances
rbk = NewsRbk()
bot = MyBot()

# Define the main coroutine that runs the bot and checks for new articles
async def main():
    if __name__ == '__main__':
        while True:
            task1 = bot.news_every_minute(rbk.get_articles())
            await task1
            await asyncio.sleep(30)

# Run the main coroutine
asyncio.run(main())
