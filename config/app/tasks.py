
from celery import shared_task
from django.utils import timezone
from config.app.models import Habits, CustomUser
from aiogram import Bot, types
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

@shared_task
def send_reminders():
    now = timezone.now().time()
    habits = Habits.objects.filter(time__lte=now, time__gte=(now - timezone.timedelta(minutes=1)))

    for habit in habits:
        user = habit.user
        if user.telegram_id:
            message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
            bot.send_message(user.telegram_id, message)
