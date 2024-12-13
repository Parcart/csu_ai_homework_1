import json
import os
import re

from dotenv import load_dotenv
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from Middleware import Middleware
from SearchEngine import SearchResult
from User import User

from Text import text
from model import LLMAnswer, LLMYandex, ResponseType
from parser import get_news


def escape_markdown_v2(text_to_escape):
    return re.sub(r'([_*\[\]()~>#+\-=|{}.!?`])', r'\\\1', text_to_escape)


load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), use_class_middlewares=True)
bot.setup_middleware(Middleware())

User._bot = bot


@bot.message_handler(commands=['start'])
def start(message, data):
    user: User = data["user"]
    user.send(text["welcome"], user.generate_main_menu())


@bot.message_handler(content_types=["text"], func=lambda message: message.text == text['news_button'])
def news(message, data):
    user: User = data["user"]
    news = get_news()
    for newa in news:
        bot.send_photo(chat_id=message.chat.id, photo=newa.image,
                       caption=f"<b>{newa.title}</b>\n\n{newa.text}\n{f'<a href="{newa.link}">Ссылка</a>'}",
                       parse_mode='HTML')
    # TODO Обращение к парсеру


@bot.message_handler(content_types=["text"], func=lambda message: message.text == text['back_button'])
def message_handler(message, data):
    user: User = data["user"]
    user.in_search = False
    user.send(text["back_text"], user.generate_main_menu())


@bot.message_handler(content_types=["text"], func=lambda message: message.text == text['search_button'])
def start_search(message, data):
    user: User = data["user"]
    user.in_search = True
    msg = user.send(text["query_search"], user.generate_search_menu())
    bot.register_next_step_handler(msg, search, data)


def search(message, data):
    user: User = data["user"]
    current_message = user.send(text["start_search"], user.generate_search_menu())

    answer = LLMYandex.processing_query(message.text)
    print("INFO: answer: " + answer)
    try:
        cleaned_json_str = answer.strip('```').strip()
        answer = LLMAnswer.model_validate_json(cleaned_json_str)
    except Exception as e:
        # bot.edit_message_text(text=answer, chat_id=current_message.chat.id, message_id=current_message.message_id)
        bot.delete_message(current_message.chat.id, current_message.message_id)
        user.send(answer, user.generate_search_menu())
        return

    if answer.response_type == ResponseType.assistent:
        bot.delete_message(current_message.chat.id, current_message.message_id)
        user.send(answer.message, user.generate_search_menu())
        return

    result: list[SearchResult] = user.search(answer.message)
    # bot.edit_message_text(text=text["end_search"], chat_id=current_message.chat.id, message_id=current_message.message_id)

    if len(result) == 0:
        bot.delete_message(current_message.chat.id, current_message.message_id)
        user.send(text["empty_search"], user.generate_search_menu())
        return

    result_answer = "Вот что мне удалось найти по вашему запросу\\!"
    for item in result:
        title = f'[{escape_markdown_v2(item.title)}]({item.link})'
        result_answer += f"\n\n{title}\n{escape_markdown_v2(item.snippet)}"

    bot.delete_message(current_message.chat.id, current_message.message_id)
    user.send(result_answer, user.generate_search_menu(), parse_mode='MarkdownV2')


@bot.message_handler(func=lambda message: True)
def message_handler(message, data):
    user = data["user"]
    if user.in_search:
        search(message, data)
        return
    user.send(text["welcome"], user.generate_main_menu())


if __name__ == '__main__':
    bot.infinity_polling()
