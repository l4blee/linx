import os
import logging
import random
from typing import Protocol

import pymongo


# Using protocols to reach work convenience
class User(Protocol):
    """
    User representative protocol.
    Must have 'id' & 'preferences' in DB Document.
    """
    id: int


class Message(Protocol):
    """
    Message representative protocol.
    """
    id: int
    user: User


class MongoDB:
    def __init__(self, conn_url):
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__qualname__)
        self.connect(conn_url)

    def connect(self, conn_url):
        self.logger.info('Connecting to MongoDB...')
        self.client = pymongo.MongoClient(conn_url)

        # Main database including 2 collections for users and preferences
        self.database = self.client.forms
        self.logger.info('Successfully connected to Mongo, going further.')

    def get_form(self, message: Message) -> User:
        """
        Must be called on each reaction message in order to get the next
        user form to be used as the Bot's answer message
        """
        user: User = message.user

        # Requesting users collection to get user preferences
        user_record = self.database.users.find_one({
            'id': user.id  # Unique userid for each document required
        })

        # Getting user's preferences to find other forms
        preferences = user_record.get('preferences')
        preference = random.choice(preferences)

        # The following code is not optimised in speed/memory
        # You may change it to speedup somehow
        user_list = self.database.preferences.find({
            'preference': preference
        })
        returnable_user = random.choice(user_list)
        # As using random, might want to check if this user wasn't suggested before

        return returnable_user
