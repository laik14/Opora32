from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from datetime import datetime
from keyboards.admin_keyboard import get_admin_keyboard, get_schedule_action_keyboard, get_back_keyboard  # Импортируем необходимые функции
from utils.calendar_utils import load_events, save_events, add_event, remove_event  # Импортируем функции из calendar_utils

# Логика для загрузки и хранения событий
EVENTS = load_events()

# Обработчик команд администратора
async def handle_admin_panel(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Подтверждаем получение запроса
    data = query.data

    if data == "admin_edit_schedule":
        # Переход в раздел редактирования расписания
        await query.edit_message_text(
            "Редактирование расписания... Выберите действие:",
            reply_markup=get_schedule_action_keyboard()
        )
    elif data == "admin_view_schedule":
        # Просмотр расписания с выводом всех событий
        keyboard = []
        if not EVENTS:
            await query.edit_message_text("Нет доступных событий для просмотра.")
            return

        for index, event in enumerate(EVENTS):
            keyboard.append([
                InlineKeyboardButton(f"Изменить {event['date']} - {event['title']} ({event['time']})", callback_data=f"edit_event_{index}"),
                InlineKeyboardButton(f"Удалить {event['date']} - {event['title']}", callback_data=f"delete_event_{index}")
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Выберите событие для редактирования или удаления:",
            reply_markup=reply_markup
        )
    elif data == "admin_exit":
        # Завершение админской сессии
        await query.edit_message_text("Выход из админ панели. Напишите /start, чтобы вернуться.")
    elif data == "admin_back":
        # Возврат в основное меню администрирования
        await query.edit_message_text(
            "Вы в админской панели. Выберите действие:",
            reply_markup=get_admin_keyboard()  # Кнопки для администрирования
        )
    elif data.startswith("edit_event_"):
        # Переход в редактирование конкретного события
        event_id = int(data.split("_")[-1])
        if 0 <= event_id < len(EVENTS):
            event = EVENTS[event_id]
            await query.edit_message_text(
                f"Редактирование события: {event['title']}. Введите новые данные.\n\n"
                "1. Для изменения названия события, введите новое название.\n"
                "2. Для изменения времени события, введите новое время в формате 'ЧЧ:ММ'.",
                reply_markup=get_back_keyboard()  # Добавляем кнопку "Назад"
            )
            context.user_data['edit_event_id'] = event_id  # Сохраняем ID события для редактирования
        else:
            await query.edit_message_text(f"Событие с ID {event_id} не найдено.")
    elif data.startswith("delete_event_"):
        # Удаление события
        event_id = int(data.split("_")[-1])
        if 0 <= event_id < len(EVENTS):
            removed_event = EVENTS.pop(event_id)  # Удаляем событие
            save_events()  # Сохраняем изменения в файл
            await query.edit_message_text(f"Событие '{removed_event['title']}' удалено.")
            # Обновляем список событий
            keyboard = []
            for index, event in enumerate(EVENTS):
                keyboard.append([
                    InlineKeyboardButton(f"Изменить {event['date']} - {event['title']} ({event['time']})", callback_data=f"edit_event_{index}"),
                    InlineKeyboardButton(f"Удалить {event['date']} - {event['title']}", callback_data=f"delete_event_{index}")
                ])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "Выберите событие для редактирования или удаления:",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text("Ошибка: событие не найдено.")
    elif data == "admin_add_event":
        # Переход к добавлению нового события
        context.user_data['add_event'] = True  # Устанавливаем флаг для добавления события
        await query.edit_message_text(
            "Введите данные для нового события в формате:\n"
            "Дата (YYYY-MM-DD)\n"
            "Название события\n"
            "Время (HH:MM)",
            reply_markup=get_back_keyboard()  # Добавляем кнопку "Назад"
        )
    else:
        await query.edit_message_text("Неизвестная команда.", reply_markup=get_admin_keyboard())

# Обработчик для редактирования или добавления события
async def handle_event_input(update: Update, context: CallbackContext):
    # Проверка на то, что пользователь пытается редактировать событие
    if 'edit_event_id' in context.user_data:
        event_id = context.user_data['edit_event_id']
        new_data = update.message.text.strip()

        # Проверяем, что ввел администратор
        if new_data:
            event = EVENTS[event_id]
            if ":" in new_data and len(new_data) == 5 and new_data[2] == ":":
                # Преобразуем строку в формат времени (часы:минуты)
                try:
                    new_time = datetime.strptime(new_data, "%H:%M").strftime("%H:%M")
                    EVENTS[event_id]['time'] = new_time
                    save_events()  # Сохраняем изменения в файл
                    await update.message.reply_text(f"Время события обновлено на {new_time}.")
                except ValueError:
                    await update.message.reply_text("Неверный формат времени. Используйте формат 'ЧЧ:ММ'.")
            else:
                EVENTS[event_id]['title'] = new_data
                save_events()  # Сохраняем изменения в файл
                await update.message.reply_text(f"Название события обновлено на '{new_data}'.")
            context.user_data['edit_event_id'] = None  # Очистка действия
        else:
            await update.message.reply_text("Пожалуйста, введите новые данные для события.")
    elif 'add_event' in context.user_data:
        # Логика для добавления нового события
        event_data = update.message.text.strip().split("\n")
        if len(event_data) == 3:
            try:
                date = event_data[0].strip()
                title = event_data[1].strip()
                time = event_data[2].strip()

                # Добавление события в список
                add_event(date, time, title)
                save_events()  # Сохраняем изменения в файл
                await update.message.reply_text(f"Новое событие '{title}' добавлено.")
                context.user_data['add_event'] = None  # Очищаем контекст добавления события
            except Exception as e:
                await update.message.reply_text(f"Ошибка при добавлении события: {e}")
        else:
            await update.message.reply_text("Неверный формат данных. Убедитесь, что вы ввели данные в формате:\nДата (YYYY-MM-DD)\nНазвание события\nВремя (HH:MM)")
