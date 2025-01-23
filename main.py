        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
        from config import TOKEN, ADMINS
        from handlers.admin import handle_admin_panel, handle_event_input
        from handlers.user import handle_user_request
        from keyboards.admin_keyboard import get_admin_keyboard
        from keyboards.user_keyboard import get_user_keyboard
        from utils.calendar_utils import load_events, save_events, add_event  # Импортируем функции для работы с событиями

        # Загружаем события из файла
        EVENTS = load_events()

        async def start(update, context):
            user_id = update.effective_user.id

            if user_id in ADMINS:
                # Админская панель
                keyboard = [
                    [InlineKeyboardButton("Добавить событие", callback_data="add_event")],
                    [InlineKeyboardButton("Добавить новость", callback_data="add_news")],
                    [InlineKeyboardButton("Редактировать событие", callback_data="edit_event")],
                    [InlineKeyboardButton("Удалить событие", callback_data="delete_event")],
                    [InlineKeyboardButton("Посмотреть события", callback_data="view_events")],
                    [InlineKeyboardButton("Посмотреть новости", callback_data="view_news")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    "Добро пожаловать в админскую панель! Выберите действие:",
                    reply_markup=reply_markup
                )
            else:
                # Панель для обычного пользователя
                keyboard = [
                    [InlineKeyboardButton("Посмотреть события", callback_data="view_events")],
                    [InlineKeyboardButton("Посмотреть новости", callback_data="view_news")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    "Добро пожаловать! Выберите действие:",
                    reply_markup=reply_markup
                )

        # Обработчик для нажатий на inline кнопки
        async def handle_inline_button(update, context):
            query = update.callback_query
            user_id = query.from_user.id

            await query.answer()  # Подтверждение получения callback_query

            if user_id in ADMINS:
                # Реакция на действия админа
                if query.data == "add_event":
                    await query.message.reply_text("Введите название нового события:", reply_markup=ReplyKeyboardRemove())
                    # Логика добавления события
                elif query.data == "add_news":
                    await query.message.reply_text("Введите новость:", reply_markup=ReplyKeyboardRemove())
                    # Логика добавления новости
                elif query.data == "edit_event":
                    await query.message.reply_text("Выберите событие для редактирования:", reply_markup=ReplyKeyboardRemove())
                    # Логика редактирования события
                elif query.data == "delete_event":
                    await query.message.reply_text("Выберите событие для удаления:", reply_markup=ReplyKeyboardRemove())
                    # Логика удаления события
                elif query.data == "view_events":
                    # Просмотр событий
                    events_text = "\n".join([event['name'] for event in EVENTS])  # Пример
                    await query.message.reply_text(f"Текущие события:\n{events_text}", reply_markup=ReplyKeyboardRemove())
                elif query.data == "view_news":
                    # Просмотр новостей
                    news_text = "Новости:\n1. Новость 1\n2. Новость 2"  # Пример
                    await query.message.reply_text(news_text, reply_markup=ReplyKeyboardRemove())
            else:
                # Реакция на действия обычного пользователя
                if query.data == "view_events":
                    event_text = "\n".join([event['name'] for event in EVENTS])  # Пример
                    await query.message.reply_text(f"Текущие события:\n{event_text}", reply_markup=ReplyKeyboardRemove())
                elif query.data == "view_news":
                    news_text = "Новости:\n1. Новость 1\n2. Новость 2"  # Пример
                    await query.message.reply_text(news_text, reply_markup=ReplyKeyboardRemove())

        def main():
            # Создание приложения
            app = Application.builder().token(TOKEN).build()

            # Обработчик команды /start
            app.add_handler(CommandHandler("start", start))

            # Обработчики для inline кнопок
            app.add_handler(CallbackQueryHandler(handle_inline_button))

            # Обработчики для пользовательских запросов (текстовые сообщения)
            app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_user_request))

            print("Бот запущен...")
            # Запуск бота
            app.run_polling()

        if __name__ == "__main__":
            main()