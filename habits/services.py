import requests
from django.conf import settings
from django.utils.timezone import localtime
from config import settings

from rest_framework import status


def send_telegram_massage(habit):
    """Отправляет сообщение в телеграм с напоминанием о привычке"""
    local_habit_time = localtime(habit.time)
    formatted_time = local_habit_time.strftime("%H:%M")

    text = f"{habit.action} запланировано на сегодня в {formatted_time}"
    chat_id = habit.user.tg_chat_id
    params = {"text": text, "chat_id": chat_id}

    response = requests.get(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", data=params
    )
    if response.status_code != status.HTTP_200_OK:
        print(f"Ошибка при отправке сообщения в Telegram: {response.text}")
