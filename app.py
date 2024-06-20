import asyncio, aioschedule
from aiogram import executor
from handlers.handler import *
from configs.bot_config import dp

async def send_msg_30():
    aioschedule.every(interval=30).minutes.do(send_message_to_groups_30)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1800)

async def send_msg_45():
    aioschedule.every(interval=45).minutes.do(send_message_to_groups_45)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2700)

async def send_msg_60():
    aioschedule.every(interval=60).minutes.do(send_message_to_groups_60)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3600)

async def check_promo_code_expire():
    aioschedule.every(interval=1).day.at("05:00").do(check_promo_code_exp)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(86400)

async def check_user_publish_day():
    aioschedule.every(interval=1).day.at("05:00").do(check_user_publsh_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(86400)

tasks = [send_msg_30(), send_msg_45(), send_msg_60(), check_promo_code_expire(), check_user_publish_day()]

async def on_stup(_):
    for task in tasks:
        asyncio.create_task(task)

if __name__ == "__main__":
    from handlers.handler import *
    # executor.start_polling(dispatcher=dp, skip_updates=True)
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_stup)
