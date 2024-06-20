from configs.settings import TOKEN
from aiogram import Bot, Dispatcher

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
