from functools import lru_cache

import telebot
from telebot.types import User as TelebotUser, Message, ReplyKeyboardMarkup

from SearchEngine import SearchEngine
from Text import text


class Singleton(type):
    @lru_cache(maxsize=50)
    def __call__(cls, *args, **kwargs):
        return super(Singleton, cls).__call__(*args, **kwargs)


class User(TelebotUser, metaclass=Singleton):
    _bot: telebot.TeleBot = None

    def __init__(self, id, is_bot, first_name, last_name=None, username=None, language_code=None,
                 can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None,
                 is_premium=None, added_to_attachment_menu=None, can_connect_to_business=None,
                 has_main_web_app=None, **kwargs):
        super().__init__(id, is_bot, first_name, last_name, username, language_code,
                 can_join_groups, can_read_all_group_messages, supports_inline_queries,
                 is_premium, added_to_attachment_menu, can_connect_to_business,
                 has_main_web_app, **kwargs)
        self.in_search = False

    @staticmethod
    def search(query: str):
        return SearchEngine.run(query)

    def send(self, text: str, keyboard=None, parse_mode=None, disable_web_page_preview=True)-> Message:

        message = text
        try:
            send: Message = self._bot.send_message(self.id,
                                                   message,
                                                   parse_mode=parse_mode,
                                                   reply_markup=keyboard,
                                                   disable_web_page_preview=disable_web_page_preview)
            return send
        except Exception as e:
            print(e)

    @staticmethod
    def generate_main_menu():
        markup_main = ReplyKeyboardMarkup(resize_keyboard=True)
        markup_main.add(text["news_button"])
        markup_main.add(text["search_button"])
        return markup_main
    
    @staticmethod
    def generate_search_menu():
        markup_main = ReplyKeyboardMarkup(resize_keyboard=True)
        markup_main.add(text["back_button"])
        return markup_main

    def generate_answer(self, text):
        pass
