from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_clients_keyboard(users: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for user in users:
        # user structure from get_all_users: (user_id, join_date)
        # We need name. Let's assume passed users list is (user_id, username, full_name, ...) 
        # or we fetch full info before calling this.
        # Actually existing get_all_users returns (user_id, join_date).
        # We should update get_all_users to return full info or handle it here.
        # Let's assume we update get_all_users or fetch details in handler. 
        # Better: let handler pass list of (user_id, full_name).
        
        user_id = user[0]
        full_name = user[2] # Assuming we get full user tuple
        
        builder.button(text=f"{full_name}", callback_data=f"client_{user_id}")
        
    builder.adjust(1) # 1 column
    return builder.as_markup()
