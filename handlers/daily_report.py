from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import db
from states.states import DailyReportState
from utils.motivation import get_random_phrase
from config import ADMIN_ID

router = Router()

@router.message(Command("daily_report"))
@router.message(F.text == "📝 Щоденний звіт")
async def start_daily_report(message: types.Message, state: FSMContext):
    await message.answer("Час для щоденного звіту! Скільки калорій ти спожив сьогодні?")
    await state.set_state(DailyReportState.calories)

@router.message(DailyReportState.calories)
async def process_calories(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Будь ласка, введи ціле число.")
        return
    await state.update_data(calories=int(message.text))
    await message.answer("Скільки білків (г)?")
    await state.set_state(DailyReportState.proteins)

@router.message(DailyReportState.proteins)
async def process_proteins(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(proteins=val)
        await message.answer("Скільки жирів (г)?")
        await state.set_state(DailyReportState.fats)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(DailyReportState.fats)
async def process_fats(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(fats=val)
        await message.answer("Скільки кроків пройшов?")
        await state.set_state(DailyReportState.steps)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(DailyReportState.steps)
async def process_steps(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Будь ласка, введи ціле число.")
        return
    await state.update_data(steps=int(message.text))
    await message.answer("Скільки тренувань було сьогодні?")
    await state.set_state(DailyReportState.workouts)

@router.message(DailyReportState.workouts)
async def process_workouts(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Будь ласка, введи ціле число.")
        return
    await state.update_data(workouts=int(message.text))
    await message.answer("Оціни свій емоційний стан (1-10):")
    await state.set_state(DailyReportState.mood)

@router.message(DailyReportState.mood)
async def process_mood(message: types.Message, state: FSMContext, bot: Bot):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Будь ласка, введи число від 1 до 10.")
        return
    
    await state.update_data(mood=int(message.text))
    data = await state.get_data()
    
    # Save Daily Report
    await db.add_daily_report(
        user_id=message.from_user.id,
        calories=data['calories'],
        proteins=data['proteins'],
        fats=data['fats'],
        steps=data['steps'],
        workouts=data['workouts'],
        mood=int(message.text)
    )
    
    # Send Report to Admin
    user_info = await db.get_user(message.from_user.id)
    full_name = user_info[2] if user_info else "Невідомий"
    
    report_text = (
        f"📋 **Новий звіт від {full_name}**\n"
        f"Калорії: {data['calories']}\n"
        f"Білки: {data['proteins']}г\n"
        f"Жири: {data['fats']}г\n"
        f"Кроки: {data['steps']}\n"
        f"Тренування: {data['workouts']}\n"
        f"Настрій: {message.text}/10"
    )
    
    await bot.send_message(chat_id=ADMIN_ID, text=report_text)
    
    await message.answer(get_random_phrase())
    await state.clear()
