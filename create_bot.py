from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv, find_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("token"))
dp = Dispatcher()

admin = list(map(int, os.getenv("admin").split(",")))

