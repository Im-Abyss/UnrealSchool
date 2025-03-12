from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сразу к делу 🟢", 
                              callback_data="start")]
])