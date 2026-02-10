from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_ID

def get_main_menu_kb(user_id: int) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="📝 Щоденний звіт"),
            KeyboardButton(text="📅 Щотижневий звіт")
        ],
        [
            KeyboardButton(text="📊 Моя статистика"),
            KeyboardButton(text="📷 Відправити фото")
        ]
    ]
    
    if user_id == ADMIN_ID:
        kb.append([
            KeyboardButton(text="👥 Клієнти"),
            KeyboardButton(text="📈 Загальна статистика")
        ])
        
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
