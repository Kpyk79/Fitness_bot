from aiogram import Router, types, F
from aiogram.filters import Command
from database import db
from config import ADMIN_ID
from keyboards.inline import get_clients_keyboard

router = Router()

@router.message(Command("clients"))
@router.message(F.text == "👥 Клієнти")
async def cmd_clients(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    users = await db.get_all_users()
    if not users:
        await message.answer("Клієнтів ще немає.")
        return

    await message.answer("Обери клієнта для перегляду статистики:", reply_markup=get_clients_keyboard(users))

@router.callback_query(F.data.startswith("client_"))
async def cb_client_stats(callback: types.CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer("Невірні дані.")
        return
    
    user = await db.get_user(user_id)
    if not user:
        await callback.answer("Клієнта не знайдено.")
        return

    # Fetch full history
    metrics_history = await db.get_all_user_metrics(user_id)
    daily_reports = await db.get_all_daily_reports(user_id)
    
    text = f"📊 **Повне досьє на {user[2]}**\n"
    text += f"Вік: {user[3]} | Стать: {user[4]} | Дата реєстрації: {user[5]}\n"
    text += "-" * 20 + "\n"

    # Metrics Analysis
    if metrics_history:
        first = metrics_history[0]
        last = metrics_history[-1]
        
        text += "📏 **Заміри (Перший -> Останній):**\n"
        # 3:waist, 4:chest, 5:belly, 6:hips, 7:l_arm, 8:r_arm, 9:l_leg, 10:r_leg
        text += f"Талія: {first[3]} -> {last[3]} ({last[3]-first[3]:+.1f})\n"
        text += f"Груди: {first[4]} -> {last[4]} ({last[4]-first[4]:+.1f})\n"
        text += f"Живіт: {first[5]} -> {last[5]} ({last[5]-first[5]:+.1f})\n"
        text += f"Стегна: {first[6]} -> {last[6]} ({last[6]-first[6]:+.1f})\n"
    else:
        text += "Даних замірів немає.\n"
        
    text += "-" * 20 + "\n"

    # Daily Reports Analysis
    if daily_reports:
        total_days = len(daily_reports)
        msg_count = len(daily_reports)
        
        avg_calories = sum(r[3] for r in daily_reports) / msg_count
        avg_steps = sum(r[6] for r in daily_reports) / msg_count
        avg_mood = sum(r[8] for r in daily_reports) / msg_count
        total_workouts = sum(r[7] for r in daily_reports)
        
        text += "📅 **Щоденна активність:**\n"
        text += f"Всього звітів: {total_days}\n"
        text += f"Сер. калорії: {int(avg_calories)}\n"
        text += f"Сер. кроки: {int(avg_steps)}\n"
        text += f"Сер. настрій: {avg_mood:.1f}/10\n"
        text += f"Всього тренувань: {total_workouts}\n"
    else:
        text += "Щоденних звітів немає.\n"

    await callback.message.edit_text(text, reply_markup=get_clients_keyboard(await db.get_all_users()))
    await callback.answer()

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Старий метод. Використовуй /clients для зручності.")

@router.message(F.text == "📈 Загальна статистика")
async def cmd_general_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    users = await db.get_all_users()
    total_users = len(users)
    
    text = (
        f"📈 **Загальна статистика бота**\n"
        f"Всього користувачів: {total_users}\n"
    )
    await message.answer(text)
