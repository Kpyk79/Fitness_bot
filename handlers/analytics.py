from aiogram import Router, types, F
from aiogram.filters import Command
from database import db

router = Router()

@router.message(Command("stats"))
@router.message(F.text == "📊 Моя статистика")
async def cmd_my_stats(message: types.Message):
    """
    Shows statistics for the user who requested it.
    """
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("Ти ще не зареєстрований! Натисни /start")
        return

    baseline = await db.get_baseline_metrics(user_id)
    current_metrics = await db.get_user_metrics(user_id, limit=1)
    
    text = f"📊 **Твоя статистика, {user[2]}**\n\n"

    if baseline and current_metrics:
        curr = current_metrics[0]
        # curr tuple structure based on db.py:
        # 0:id, 1:user_id, 2:date, 3:waist, 4:chest, 5:belly, 6:hips, 
        # 7:l_arm, 8:r_arm, 9:l_leg, 10:r_leg, 11:is_baseline
        
        text += "**Зміни параметрів (від старту):**\n"
        
        diff_waist = curr[3] - baseline[3]
        text += f"Талія: {curr[3]} см ({diff_waist:+.1f})\n"
        
        diff_chest = curr[4] - baseline[4]
        text += f"Груди: {curr[4]} см ({diff_chest:+.1f})\n"
        
        diff_belly = curr[5] - baseline[5]
        text += f"Живіт: {curr[5]} см ({diff_belly:+.1f})\n"
        
        diff_hips = curr[6] - baseline[6]
        text += f"Стегна: {curr[6]} см ({diff_hips:+.1f})\n"
        
    else:
        text += "Ще недостатньо даних для порівняння замірів.\n"
        if not baseline:
            text += "(Не знайдено базових замірів)\n"

    # Daily Activity Averages (Last 7 days)
    reports = await db.get_daily_reports(user_id, limit=7)
    if reports:
        # reports tuple: 0:id, 1:user_id, 2:date, 3:calories, 4:proteins, 5:fats, 6:steps, 7:workouts, 8:mood
        avg_steps = sum(r[6] for r in reports) / len(reports)
        avg_mood = sum(r[8] for r in reports) / len(reports)
        # avg_calories is a good metric too
        avg_calories = sum(r[3] for r in reports) / len(reports)
        
        text += f"\n**Середнє за останні 7 днів:**\n"
        text += f"👣 Кроки: {int(avg_steps)}\n"
        text += f"🔥 Калорії: {int(avg_calories)}\n"
        text += f"😊 Настрій: {avg_mood:.1f}/10\n"
    else:
        text += "\nНемає даних щоденних звітів за останній тиждень."
    
    await message.answer(text)