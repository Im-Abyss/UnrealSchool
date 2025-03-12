import asyncio
from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Ai(StatesGroup):

    response = State()


class Post(StatesGroup):

    create = State()


import app.keyboards as kb

from .ai import get_completion


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! 😊✨\n\nДобро пожаловать в нашу онлайн-школу по разработке игр на Unreal Engine 5, где мечты становятся реальностью! 🎮💻\n\nЗдесь ты научишься создавать потрясающие миры, оживлять персонажей и воплощать свои идеи в жизнь. �‍💻🌟\n\nМы поможем тебе стать настоящим мастером геймдева и открыть двери в индустрию игр. 🚀📚\n\nДавай создавать будущее игр вместе! #UnrealEngine5 #Геймдев 💡🌍",
                         reply_markup=kb.main_keyboard)
    

@router.message(Command("help"))
async def help_commands(message: Message):
    pass


@router.message(Command("ai"))
async def help_ai(message: Message, state: FSMContext):
    await message.answer("Привет, вот что я могу:\n\n- Отвечать на вопросы по Unreal Engine 5\n- Помогать с техническими вопросами\n- Предоставлять полезные советы и рекомендации\n- Отвечать на вопросы по геймдеву")
    await state.set_state(Ai.response)


@router.message(StateFilter(Ai.response))
async def help_ai(message: Message, state: FSMContext):
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


@router.message(Command("post"))
async def help_commands(message: Message, state: FSMContext):

    await message.answer("Напишите текст для вашего поста")
    await state.set_state(Post.create)



@router.message(StateFilter(Post.create))
async def help_ai(message: Message, state: FSMContext, bot: Bot):

    await state.update_data(post=message.text)
    data = await state.get_data()

    await bot.send_message(chat_id='-1002024259566', text=data.get('post'))
    await state.clear()