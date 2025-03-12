import asyncio
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from .ai import get_completion


class Ai(StatesGroup):
    response = State()


class Post(StatesGroup):
    confirm = State()
    create = State()


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! 😊✨\n\nДобро пожаловать в нашу онлайн-школу по разработке игр на Unreal Engine 5, где мечты становятся реальностью! 🎮💻\n\n"
        "Здесь ты научишься создавать потрясающие миры, оживлять персонажей и воплощать свои идеи в жизнь. 💡🌍\n\n"
        "Мы поможем тебе стать настоящим мастером геймдева и открыть двери в индустрию игр. 🚀📚\n\n"
        "Давай создавать будущее игр вместе! #UnrealEngine5 #Геймдев",
        reply_markup=kb.main_keyboard
    )


@router.message(Command("help"))
async def help_commands(message: Message):
    await message.answer("""📌 Список доступных команд:
🔹 /start – Начать
Эта команда запускает бота и отправляет приветственное сообщение. Вы узнаете, чем может помочь бот, и получите доступ к основному меню.

🔹 /help – Помощь
Позволяет узнать, какие функции доступны в боте. Здесь можно получить инструкцию по использованию и список команд с их описанием.

🔹 /ai – AI-помощник
Запускает интеллектуального помощника, который может:
— Отвечать на вопросы по Unreal Engine 5
— Давать советы по разработке игр
— Помогать с техническими вопросами
— Объяснять ключевые аспекты геймдева

🔹 /post – Создать пост
Позволяет создать текстовый пост для Telegram-канала. Бот предложит вам написать описание, сгенерирует текст, а затем вы сможете либо утвердить его, либо попросить переделать.

💡 Обратите внимание! Внизу слева есть кнопка "Меню", где можно быстро выбрать нужную команду. 🚀""")


@router.message(Command("ai"))
async def ai_start(message: Message, state: FSMContext):
    await message.answer(
        "Привет, вот что я могу:\n\n- Отвечать на вопросы по Unreal Engine 5\n- Помогать с техническими вопросами\n"
        "- Предоставлять полезные советы и рекомендации\n- Отвечать на вопросы по геймдеву"
    )
    await state.set_state(Ai.response)


@router.message(StateFilter(Ai.response))
async def ai_response(message: Message, state: FSMContext):
    loading_message = await message.answer('Думаю...')
    await asyncio.sleep(1)
    await waiting(loading_message)
    response = await get_completion(message.text)
    await message.answer(response)
    await state.clear()


async def waiting(message: Message):
    loading_list = ['Думаю.', 'Думаю..', 'Думаю...']
    for phrase in loading_list:
        await message.edit_text(text=phrase)
        await asyncio.sleep(1)