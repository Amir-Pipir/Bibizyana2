import asyncio
from create_bot import dp, bot
from database.engine import drop_db, create_db, session_maker
from middlewares.db import DataBaseSession
from handlers import users, admin

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from middlewares.apshed import SchedulerMiddleware
from apscheduler.triggers.cron import CronTrigger

from database.orm_query import orm_get_all_users, orm_update_status

from monkey import monkey
import random

dp.include_router(users.user_router)
dp.include_router(admin.admin_router)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def send_monkey():
    print("Начинаю рассылку")

    async with session_maker() as session:
        all_users = await orm_get_all_users(session)

    for user in all_users:
        if user.monkey_status:
            try:
                random_monkey = random.choice(monkey)
                await bot.send_sticker(user.tg_id, random_monkey["sticker_id"])
                await bot.send_message(user.tg_id, random_monkey["text"])
            except:
                continue


async def update_status_00am():
    print("Начинаю обновлять статусы")

    async with session_maker() as session:
        all_users = await orm_get_all_users(session)
        for user in all_users:
            await orm_update_status(session, user.tg_id, True)


async def on_startup():
    run = False
    if run:
        await drop_db()
    await create_db()
    scheduler.start()
    scheduler.add_job(send_monkey, CronTrigger.from_crontab('0 12 * * *'))
    scheduler.add_job(update_status_00am, CronTrigger.from_crontab('1 0 * * *'))
    print("Бот вышел в онлайн")


async def main():
    dp.startup.register(on_startup)
    dp.update.middleware(SchedulerMiddleware(scheduler))
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключился")
