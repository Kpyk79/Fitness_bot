from aiogram import Router, types, F, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from database import db
from states.states import PhotoState
from config import ADMIN_ID
from keyboards.reply import get_main_menu_kb

router = Router()

@router.message(F.text == "📷 Відправити фото")
async def start_photo_sending(message: types.Message, state: FSMContext):
    await message.answer("Надішли мені фото (можеш додати підпис).", reply_markup=ReplyKeyboardRemove())
    await state.set_state(PhotoState.waiting_for_photo)

@router.message(PhotoState.waiting_for_photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    file_id = photo.file_id
    caption = message.caption
    
    # Save to DB
    await db.add_photo(user_id=message.from_user.id, photo_id=file_id, caption=caption)
    
    # Forward to Admin
    user_info = await db.get_user(message.from_user.id)
    full_name = user_info[2] if user_info else "Невідомий"
    username = f"@{user_info[1]}" if user_info and user_info[1] else ""
    
    admin_caption = f"📸 **Нове фото від {full_name}** {username}\n"
    if caption:
        admin_caption += f"Підпис: {caption}"
        
    await bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=admin_caption)
    
    await message.answer("Фото отримано і відправлено тренеру! Дякую.", reply_markup=get_main_menu_kb(message.from_user.id))
    await state.clear()

@router.message(PhotoState.waiting_for_photo)
async def process_not_photo(message: types.Message):
    await message.answer("Будь ласка, надішли саме фото.")
