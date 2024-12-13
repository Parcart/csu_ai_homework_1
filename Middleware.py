import asyncio
import threading
import time
from queue import Queue
from threading import Lock

from telebot.handler_backends import BaseMiddleware
from telebot.types import Message, CallbackQuery

from User import User


class Middleware(BaseMiddleware):
    active_tasks = []
    block_queue = False

    def __init__(self):
        super().__init__()
        self.update_types = ['message', 'callback_query']

    def pre_process(self, message, data):
        while True:
            if message.from_user.id in self.active_tasks or self.block_queue:
                continue
            try:
                self.active_tasks.append(message.from_user.id)
                user = User(**message.from_user.to_dict())
                data["user"] = user
            finally:
                self.active_tasks.remove(message.from_user.id)
            break

    def post_process(self, message, data, exception=None):
        if exception:
            print(exception)
