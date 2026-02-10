from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import db
from states.states import OnboardingState
from keyboards.reply import get_main_menu_kb

router = Router()

@router.message(OnboardingState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Скільки тобі років?")
    await state.set_state(OnboardingState.age)

@router.message(OnboardingState.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Будь ласка, введи число.")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Твоя стать (Чоловік/Жінка)?")
    await state.set_state(OnboardingState.gender)

@router.message(OnboardingState.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Тепер заміри. Обхват талії (см)?")
    await state.set_state(OnboardingState.waist)

@router.message(OnboardingState.waist)
async def process_waist(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(waist=val)
        await message.answer("Обхват грудей (см)?")
        await state.set_state(OnboardingState.chest)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.chest)
async def process_chest(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(chest=val)
        await message.answer("Обхват низу живота (см)?")
        await state.set_state(OnboardingState.belly)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.belly)
async def process_belly(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(belly=val)
        await message.answer("Обхват стегон (см)?")
        await state.set_state(OnboardingState.hips)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.hips)
async def process_hips(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(hips=val)
        await message.answer("Обхват лівої руки (см)?")
        await state.set_state(OnboardingState.l_arm)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.l_arm)
async def process_l_arm(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(l_arm=val)
        await message.answer("Обхват правої руки (см)?")
        await state.set_state(OnboardingState.r_arm)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.r_arm)
async def process_r_arm(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(r_arm=val)
        await message.answer("Обхват лівої ноги (см)?")
        await state.set_state(OnboardingState.l_leg)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.l_leg)
async def process_l_leg(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(l_leg=val)
        await message.answer("Обхват правої ноги (см)?")
        await state.set_state(OnboardingState.r_leg)
    except ValueError:
        await message.answer("Будь ласка, введи число.")

@router.message(OnboardingState.r_leg)
async def process_r_leg(message: types.Message, state: FSMContext):
    try:
        val = float(message.text.replace(',', '.'))
        await state.update_data(r_leg=val)
        
        data = await state.get_data()
        
        # Save User
        await db.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=data['name'],
            age=data['age'],
            gender=data['gender']
        )
        
        # Save Baseline Metrics
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
            is_baseline=True
        )
        
        await message.answer("Чудово! Твої дані збережено. Я буду нагадувати тобі про звіти.", reply_markup=get_main_menu_kb(message.from_user.id))
        await state.clear()
        
    except ValueError:
        await message.answer("Будь ласка, введи число.")
