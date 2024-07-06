# bot.py

import os
import django
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.core.paginator import Paginator
from config.app.models import CustomUser, Habits

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_django_project.settings')
django.setup()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ITEMS_PER_PAGE = 5


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user, created = CustomUser.objects.get_or_create(username=message.from_user.username)
    user.telegram_id = message.from_user.id
    user.save()
    await message.answer("Ваш аккаунт привязан к этому боту.")


@dp.message_handler(commands=['habits'])
async def list_habits(message: types.Message):
    await send_habits_page(message, page_number=1)


@dp.callback_query_handler(lambda c: c.data.startswith('page:'))
async def process_page(callback_query: types.CallbackQuery):
    page_number = int(callback_query.data.split(':')[1])
    await send_habits_page(callback_query.message, page_number)
    await callback_query.answer()


async def send_habits_page(message, page_number=1):
    user = CustomUser.objects.get(telegram_id=message.from_user.id)
    habits = Habits.objects.filter(user=user)
    paginator = Paginator(habits, ITEMS_PER_PAGE)

    if page_number > paginator.num_pages or page_number < 1:
        page_number = 1

    page = paginator.page(page_number)
    habits_list = "\n".join([f"{habit.action} at {habit.time} in {habit.place}" for habit in page.object_list])

    markup = InlineKeyboardMarkup()
    if page.has_previous():
        markup.add(InlineKeyboardButton("Previous", callback_data=f'page:{page.previous_page_number()}'))
    if page.has_next():
        markup.add(InlineKeyboardButton("Next", callback_data=f'page:{page.next_page_number()}'))

    await message.answer(habits_list, reply_markup=markup)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
