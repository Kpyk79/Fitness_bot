import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from config import BOT_TOKEN
from database import db
from handlers import common, onboarding, daily_report, admin, weekly_report, analytics, photos

# Configure logging
logging.basicConfig(level=logging.INFO)

# Київський часовий пояс
KYIV_TZ = timezone('Europe/Kiev')

async def check_daily_reminders(bot: Bot):
    users = await db.get_all_users()
    for user in users:
        user_id = user[0]
        try:
            await bot.send_message(
                chat_id=user_id,
                text="🔔 Привіт! Не забудь надіслати щоденний звіт. Натисни /daily_report"
            )
        except Exception as e:
            logging.error(f"Failed to send daily reminder to {user_id}: {e}")

async def check_weekly_reminders(bot: Bot):
    users = await db.get_all_users()
    today = datetime.now().date()
    
    for user in users:
        user_id = user[0]
        join_date_str = user[1]
        
        try:
            join_date = datetime.strptime(join_date_str, "%Y-%m-%d").date()
            days_since_join = (today - join_date).days
            
            # If it's the 7th day (and multiples of 7), send reminder
            if days_since_join > 0 and days_since_join % 7 == 0:
                await bot.send_message(
                    chat_id=user_id,
                    text="📅 Минув тиждень! Час оновити заміри. Натисни /weekly_report"
                )
        except Exception as e:
            logging.error(f"Failed to send weekly reminder to {user_id}: {e}")

async def main():
    # Initialize DB
    await db.init_db()

    # Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Include Routers
    dp.include_router(common.router)
    dp.include_router(onboarding.router)
    dp.include_router(daily_report.router)
    dp.include_router(weekly_report.router)
    dp.include_router(analytics.router)
    dp.include_router(photos.router)
    dp.include_router(admin.router)

    # Initialize Scheduler
    scheduler = AsyncIOScheduler(timezone=KYIV_TZ)
    
    # Daily reminder at 21:00 Kyiv time
    scheduler.add_job(check_daily_reminders, 'cron', hour=21, minute=0, args=[bot])
    
    # Weekly check logic runs every day at 21:00 Kyiv time (to catch the 7th day)
    scheduler.add_job(check_weekly_reminders, 'cron', hour=21, minute=0, args=[bot])
    
    scheduler.start()

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
