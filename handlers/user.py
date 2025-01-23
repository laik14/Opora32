from telegram import Update
from telegram.ext import CallbackContext
from utils.calendar_utils import generate_calendar
from utils.map_utils import get_map_link  # Для отправки ссылки на карту
from keyboards.user_keyboard import get_user_keyboard

# Пример координат для Брянска, ул. Центральная 1в
latitude = 53.252090
longitude = 34.371670
address = "Брянск, ул. Центральная 1в"

# Обработчик пользовательских запросов
async def handle_user_request(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Расписание":
        calendar_text, event_info = generate_calendar()
        await update.message.reply_text(
            f"{event_info}\n\nКалендарь:\n```\n{calendar_text}\n```",
            parse_mode="Markdown"
        )
    elif text == "Контакты":
        await update.message.reply_text(
            "Контакты:\n"
            "[Станислав](https://t.me/Zingelstein) — Администратор",
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            "[Анна Александровна](https://t.me/AnnaPovaley) — Психолог",
            parse_mode="Markdown"
        )
    elif text == "Адрес":
        # Отправка текста с адресом
        address_text = "Брянск, ул. Центральная, 1в"
        await update.message.reply_text(f"Адрес: {address_text}")

        # Отправка точного местоположения
        await update.message.reply_location(latitude=53.256792, longitude=34.313202)
        # Или, если хотите оставить ссылку:
        # map_link = get_map_link(latitude, longitude)
        # await update.message.reply_text(f"Адрес: [Посмотреть на карте]({map_link})", parse_mode="Markdown")
    else:
        await update.message.reply_text("Я не понимаю эту команду.")
