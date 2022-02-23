# import random

import pymongo
import os
from dotenv import load_dotenv

load_dotenv('.env')

# Подрубаемся к Монго
url = os.getenv('DATABASE_URL') % {
        'username': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD')
}
print(url)
client = pymongo.MongoClient(url)
# Формат ссылки подключения думаю знаешь
# mongodb+srv://<пользователь>:<пароль>@<адрес кластера>/<имя датабазы, необязательно>?retryWrites=true&w=majority

database = client.test

print(database.reviews.find_one({
        'first': 5
})['second'])
# print(client.admin.command('serverStatus'))

database.reviews.insert_one({
        'list': [1, 2, 3]
})
