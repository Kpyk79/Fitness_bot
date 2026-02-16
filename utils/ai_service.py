import google.generativeai as genai
from config import GEMINI_API_KEY
import logging

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def analyze_client_data(user_data: tuple, metrics_history: list, daily_reports: list) -> str:
    """
    Comprehensive AI analysis of client data.
    Returns formatted analysis with recommendations.
    """
    try:
        # Prepare data for AI
        user_id, username, full_name, age, gender, join_date = user_data
        
        # Build context
        context = f"""Ти - професійний фітнес-тренер та дієтолог. Проаналізуй дані клієнта та надай детальні рекомендації українською мовою.

**Клієнт:** {full_name}
**Вік:** {age} років
**Стать:** {gender}
**Дата реєстрації:** {join_date}

"""
        
        # Add metrics analysis
        if metrics_history:
            first = metrics_history[0]
            last = metrics_history[-1]
            context += f"""**Динаміка замірів (перший → останній):**
- Талія: {first[3]} см → {last[3]} см ({last[3]-first[3]:+.1f} см)
- Груди: {first[4]} см → {last[4]} см ({last[4]-first[4]:+.1f} см)
- Живіт: {first[5]} см → {last[5]} см ({last[5]-first[5]:+.1f} см)
- Стегна: {first[6]} см → {last[6]} см ({last[6]-first[6]:+.1f} см)

"""
        
        # Add daily reports analysis
        if daily_reports:
            total_days = len(daily_reports)
            avg_calories = sum(r[3] for r in daily_reports) / total_days
            avg_proteins = sum(r[4] for r in daily_reports) / total_days
            avg_fats = sum(r[5] for r in daily_reports) / total_days
            avg_steps = sum(r[6] for r in daily_reports) / total_days
            avg_mood = sum(r[8] for r in daily_reports) / total_days
            total_workouts = sum(r[7] for r in daily_reports)
            
            context += f"""**Щоденна активність (за {total_days} днів):**
- Середні калорії: {int(avg_calories)} ккал
- Середні білки: {avg_proteins:.1f} г
- Середні жири: {avg_fats:.1f} г
- Середні кроки: {int(avg_steps)}
- Середній настрій: {avg_mood:.1f}/10
- Всього тренувань: {total_workouts}

"""
        
        prompt = context + """
Надай детальний аналіз та рекомендації у такому форматі:

🎯 **ЗАГАЛЬНА ОЦІНКА**
[Короткий висновок про прогрес]

📊 **АНАЛІЗ ЗАМІРІВ**
[Оцінка динаміки тіла]

🍽️ **ХАРЧУВАННЯ**
[Аналіз калорій, білків, жирів. Рекомендації по коригуванню]

🏃 **АКТИВНІСТЬ**
[Оцінка кроків та тренувань. Поради щодо вправ]

💪 **РЕКОМЕНДАЦІЇ**
[Конкретні дії для покращення результатів]

Будь конкретним, мотивуючим та професійним. Максимум 300 слів.
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logging.error(f"AI analysis error: {e}")
        return "❌ Помилка генерації AI аналізу. Спробуйте пізніше."


async def generate_weekly_report(user_data: tuple, metrics_history: list, daily_reports: list) -> str:
    """
    Generate weekly motivational report with recommendations.
    """
    try:
        user_id, username, full_name, age, gender, join_date = user_data
        
        # Get last 7 days of reports
        recent_reports = daily_reports[-7:] if len(daily_reports) >= 7 else daily_reports
        
        if not recent_reports:
            return f"📊 Щотижневий звіт для {full_name}\n\nНедостатньо даних для аналізу."
        
        # Calculate weekly stats
        days_count = len(recent_reports)
        avg_calories = sum(r[3] for r in recent_reports) / days_count
        avg_steps = sum(r[6] for r in recent_reports) / days_count
        avg_mood = sum(r[8] for r in recent_reports) / days_count
        total_workouts = sum(r[7] for r in recent_reports)
        
        prompt = f"""Ти - мотивуючий фітнес-тренер. Створи щотижневий звіт для клієнта {full_name}.

**Статистика за тиждень:**
- Днів звітності: {days_count}/7
- Середні калорії: {int(avg_calories)} ккал
- Середні кроки: {int(avg_steps)}
- Тренувань: {total_workouts}
- Середній настрій: {avg_mood:.1f}/10

Створи мотивуюче повідомлення у форматі:

🌟 **ЩОТИЖНЕВИЙ ЗВІТ**

📈 **ТВОЇ ДОСЯГНЕННЯ**
[Відзнач позитивні моменти]

💡 **ПОРАДИ НА НАСТУПНИЙ ТИЖДЕНЬ**
[2-3 конкретні поради]

🔥 **МОТИВАЦІЯ**
[Мотивуюче завершення]

Максимум 200 слів. Будь позитивним та підтримуючим!
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logging.error(f"Weekly report error: {e}")
        return "❌ Помилка генерації щотижневого звіту."


async def answer_question(user_data: tuple, metrics_history: list, daily_reports: list, question: str) -> str:
    """
    Answer admin's question about specific client.
    """
    try:
        user_id, username, full_name, age, gender, join_date = user_data
        
        # Build context (similar to analyze_client_data but shorter)
        context = f"""Ти - фітнес-консультант. Відповідай на питання тренера про клієнта.

**Клієнт:** {full_name}, {age} років, {gender}

"""
        
        if metrics_history:
            first = metrics_history[0]
            last = metrics_history[-1]
            context += f"**Заміри:** Талія {first[3]}→{last[3]}, Груди {first[4]}→{last[4]}, Живіт {first[5]}→{last[5]}\n"
        
        if daily_reports:
            recent = daily_reports[-7:]
            avg_cal = sum(r[3] for r in recent) / len(recent)
            avg_steps = sum(r[6] for r in recent) / len(recent)
            context += f"**Активність:** ~{int(avg_cal)} ккал, ~{int(avg_steps)} кроків/день\n"
        
        prompt = context + f"\n**Питання тренера:** {question}\n\nДай коротку, конкретну відповідь (до 150 слів):"
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logging.error(f"Question answering error: {e}")
        return "❌ Помилка обробки питання."
