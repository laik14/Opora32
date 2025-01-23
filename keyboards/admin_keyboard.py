from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_admin_keyboard():
    """Основная клавиатура админской панели"""
    keyboard = [
        [InlineKeyboardButton("Добавить событие", callback_data="admin_add_event")],
        [InlineKeyboardButton("Добавить новость", callback_data="admin_add_news")],
        [InlineKeyboardButton("Редактировать событие", callback_data="admin_edit_event")],
        [InlineKeyboardButton("Удалить событие", callback_data="admin_delete_event")],
        [InlineKeyboardButton("Выйти", callback_data="admin_exit")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Клавиатура с кнопкой 'Назад'"""
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="admin_back")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_schedule_action_keyboard():
    """Клавиатура для просмотра расписания с действиями (изменить, удалить)"""
    keyboard = [
        [InlineKeyboardButton("Добавить событие", callback_data="admin_add_event")],
        [InlineKeyboardButton("Просмотреть события", callback_data="admin_view_schedule")],
        [InlineKeyboardButton("Назад", callback_data="admin_back")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_event_action_keyboard(event_id):
    """Клавиатура для действий с конкретным событием (редактирование, удаление)"""
    keyboard = [
        [InlineKeyboardButton("Изменить", callback_data=f"edit_event_{event_id}")],
        [InlineKeyboardButton("Удалить", callback_data=f"delete_event_{event_id}")],
        [InlineKeyboardButton("Назад", callback_data="admin_back")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_news_action_keyboard():
    """Клавиатура для действий с новостями (добавить, редактировать)"""
    keyboard = [
        [InlineKeyboardButton("Добавить новость", callback_data="admin_add_news")],
        [InlineKeyboardButton("Редактировать новость", callback_data="admin_edit_news")],
        [InlineKeyboardButton("Назад", callback_data="admin_back")],
    ]
    return InlineKeyboardMarkup(keyboard)
