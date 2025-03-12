import asyncio
from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from config import CHANEL_ID
from .ai import get_completion, post_for_tg_chanel


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
    await message.answer("Список доступных команд: \n/start - Начать\n/help - Помощь\n/ai - AI-помощник\n/post - Создать пост")


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


@router.message(Command("post"))
async def post_start(message: Message, state: FSMContext):
    await message.answer("Напишите текст для вашего поста")
    await state.set_state(Post.confirm)


@router.message(StateFilter(Post.confirm))
async def post_generate(message: Message, state: FSMContext):
    await state.update_data(post=message.text)
    waiting_post = await message.answer("Пишу пост, пару секунд...")
    result = await post_for_tg_chanel(message.text)
    await state.update_data(post_result=result)
    await waiting_post.edit_text(text=result, reply_markup=kb.confirm_post)
    await state.set_state(Post.create)


@router.callback_query(F.data == "public")
async def publish_post(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    post_text = data.get("post_result")

    if post_text:
        await bot.send_message(chat_id=CHANEL_ID, text=post_text)
        await callback.message.edit_text("Всё, пост опубликован")
        await state.clear()
    else:
        await callback.answer("Ошибка: нет поста для публикации", show_alert=True)


@router.callback_query(F.data == "remake")
async def remake_post(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    original_text = data.get("post")

    if not original_text:
        await callback.answer("Ошибка: нет исходного текста для генерации", show_alert=True)
        return

    waiting_post = await callback.message.edit_text("Перегенерирую пост, пару секунд...")
    await asyncio.sleep(1)

    new_result = await post_for_tg_chanel(original_text)
    await state.update_data(post_result=new_result)
    await waiting_post.edit_text(text=new_result, reply_markup=kb.confirm_post)
