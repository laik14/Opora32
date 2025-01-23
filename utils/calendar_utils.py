import calendar
from datetime import datetime

# Список событий в памяти
EVENTS = []

def load_events():
    """Загружает события, используя хранимую в памяти переменную EVENTS."""
    return EVENTS

def save_events(events=None):
    """Сохраняет события. Если события не переданы, сохраняет текущий список EVENTS."""
    global EVENTS
    if events is not None:
        EVENTS = events

def generate_calendar():
    """Генерация календаря с событиями."""
    today = datetime.now().date()

    # Поиск ближайшего события
    upcoming_event = next(
        (event for event in EVENTS if datetime.strptime(event["date"], "%Y-%m-%d").date() >= today),
        None,
    )

    if upcoming_event:
        event_date = datetime.strptime(upcoming_event["date"], "%Y-%m-%d").strftime("%d.%m.%Y")
        event_info = f"Ближайшее событие: {upcoming_event['title']} \nДата: {event_date} \nВремя: {upcoming_event['time']}"
    else:
        event_info = "Ближайших событий не запланировано."

    # Формирование текста календаря
    cal = calendar.TextCalendar()
    current_month = today.month
    current_year = today.year
    calendar_text = cal.formatmonth(current_year, current_month)

    # Подсветка событий в календаре
    for event in EVENTS:
        event_day = int(event["date"].split("-")[2])
        calendar_text = calendar_text.replace(f" {event_day} ", f"[{event_day}]")

    return calendar_text, event_info

def add_event(date, time, title):
    """Добавление нового события в расписание."""
    new_event = {
        "date": date,
        "time": time,
        "title": title
    }
    EVENTS.append(new_event)
    save_events()  # Сохраняем изменения в памяти

def remove_event(date):
    """Удаление события по дате."""
    global EVENTS
    EVENTS = [event for event in EVENTS if event["date"] != date]
    save_events()  # Сохраняем изменения в памяти

def get_events():
    """Получить все события."""
    return EVENTS

def get_events_for_month(month, year):
    """Получить все события для определенного месяца и года."""
    return [event for event in EVENTS if datetime.strptime(event["date"], "%Y-%m-%d").month == month and datetime.strptime(event["date"], "%Y-%m-%d").year == year]
