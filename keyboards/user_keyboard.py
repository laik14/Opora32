from telegram import ReplyKeyboardMarkup

# Создание клавиатуры для пользователя
def get_user_keyboard():
    keyboard = [
        ["Расписание", "Контакты"],
        ["Адрес"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)