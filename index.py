import os
import logging

if os.getenv('APP_STATUS', 'production') != 'production':
    from dotenv import load_dotenv
    load_dotenv('.env')

from database import MongoDB
from core import Client

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s:\t%(message)s',
                    datefmt='%d.%b.%Y %H:%M:%S')

client = MongoDB(
    os.getenv('DATABASE_URL') % {
        'username': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD')
    }
)

bot = Client(client, token=os.getenv('TOKEN'))
bot.run()
