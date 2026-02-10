from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import db
from states.states import OnboardingState
from keyboards.reply import get_main_menu_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user:
        await message.answer(f"З поверненням, {user[2]}! Я готовий до роботи.", reply_markup=get_main_menu_kb(message.from_user.id))
    else:
        await message.answer(
            "Привіт! Я твій фітнес-бот. Давай познайомимось.\n"
            "Як тебе звати (ПІБ)?"
        )
        await state.set_state(OnboardingState.name)
