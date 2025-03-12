from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать обучение 🟢", 
                              callback_data="start")]
])

confirm_post = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Публикуем", 
                              callback_data="public")],
        [InlineKeyboardButton(text="Переделай", 
                              callback_data="remake")]
])