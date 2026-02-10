from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import db
from states.states import WeeklyReportState

router = Router()

# This would likely be triggered by a callback or command from the scheduler notification
# For now, let's assume the scheduler sends a message with a button that triggers a command, e.g., /weekly_report
# Or we just start the state directly if we could (but we can't easily start state from scheduler for user without an event).
# Best pattern: Scheduler sends message "Time for weekly check! Click /weekly_report to start."

@router.message(Command("weekly_report"))
@router.message(F.text == "📅 Щотижневий звіт")
async def start_weekly_report(message: types.Message, state: FSMContext):
    await message.answer("Щотижневий чек-ап! Обхват талії (см)?")
    await state.set_state(WeeklyReportState.waist)

@router.message(WeeklyReportState.waist)
async def week_waist(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(waist=val)
        await message.answer("Обхват грудей (см)?")
        await state.set_state(WeeklyReportState.chest)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.chest)
async def week_chest(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(chest=val)
        await message.answer("Обхват низу живота (см)?")
        await state.set_state(WeeklyReportState.belly)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.belly)
async def week_belly(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(belly=val)
        await message.answer("Обхват стегон (см)?")
        await state.set_state(WeeklyReportState.hips)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.hips)
async def week_hips(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(hips=val)
        await message.answer("Обхват лівої руки (см)?")
        await state.set_state(WeeklyReportState.l_arm)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.l_arm)
async def week_l_arm(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(l_arm=val)
        await message.answer("Обхват правої руки (см)?")
        await state.set_state(WeeklyReportState.r_arm)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.r_arm)
async def week_r_arm(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(r_arm=val)
        await message.answer("Обхват лівої ноги (см)?")
        await state.set_state(WeeklyReportState.l_leg)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.l_leg)
async def week_l_leg(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(l_leg=val)
        await message.answer("Обхват правої ноги (см)?")
        await state.set_state(WeeklyReportState.r_leg)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(WeeklyReportState.r_leg)
async def week_r_leg(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(r_leg=val)
        
        data = await state.get_data()
        
        # Save Metrics (is_baseline=False)
        await db.add_metrics(
            user_id=message.from_user.id,
            waist=data['waist'],
            chest=data['chest'],
            belly=data['belly'],
            hips=data['hips'],
            l_arm=data['l_arm'],
            r_arm=data['r_arm'],
            l_leg=data['l_leg'],
            r_leg=val,
            is_baseline=False
        )
        
        await message.answer("Дані оновлено! Продовжуй в тому ж дусі!")
        await state.clear()
        
    except ValueError:
        await message.answer("Будь ласка, введи число.")
from aiogram.filters import Command
