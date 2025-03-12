import asyncio
from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import app.keyboards as kb
from config import CHANEL_ID, ADMIN_ID
from .ai import post_for_tg_chanel


class Ai(StatesGroup):
    response = State()


class Post(StatesGroup):
    confirm = State()
    create = State()


admin = Router()


@admin.message(Command("post"))
async def post_start(message: Message, state: FSMContext):

    user = message.from_user.id
    
    if user == ADMIN_ID:
        await message.answer("Отправьте текст для поста")
        await state.set_state(Post.confirm)
    else:
        await message.answer("У вас нет прав для использования этой команды")


@admin.message(StateFilter(Post.confirm))
async def post_generate(message: Message, state: FSMContext):
    await state.update_data(post=message.text)
    waiting_post = await message.answer("Пишу пост, пару секунд...")
    result = await post_for_tg_chanel(message.text)
    await state.update_data(post_result=result)
    await waiting_post.edit_text(text=result, reply_markup=kb.confirm_post)
    await state.set_state(Post.create)


@admin.callback_query(F.data == "public")
async def publish_post(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    post_text = data.get("post_result")

    if post_text:
        await bot.send_message(chat_id=CHANEL_ID, text=post_text)
        await callback.message.edit_text("Всё, пост опубликован")
        await state.clear()
    else:
        await callback.answer("Ошибка: нет поста для публикации", show_alert=True)


@admin.callback_query(F.data == "remake")
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