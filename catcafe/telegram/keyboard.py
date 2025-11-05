from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Главное меню
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🐱 Посмотреть котов"))
    builder.add(KeyboardButton(text="🏠 Приютить кота"))
    builder.add(KeyboardButton(text="📍 Локация приюта"))
    builder.add(KeyboardButton(text="🌐 Сайт котокафе"))
    builder.adjust(1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


# Меню фильтров для котов
def cats_filter_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Пол", callback_data="filter_gender"))
    builder.add(InlineKeyboardButton(text="Порода", callback_data="filter_breed"))
    builder.add(InlineKeyboardButton(text="Возраст", callback_data="filter_age"))
    builder.add(InlineKeyboardButton(text="Дружелюбность", callback_data="filter_temperament"))
    builder.add(InlineKeyboardButton(text="Показать всех котов", callback_data="show_all_cats"))
    builder.adjust(2, 2, 1)
    return builder.as_markup()


# Фильтр по полу
def gender_filter_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Мальчик", callback_data="gender_male"))
    builder.add(InlineKeyboardButton(text="Девочка", callback_data="gender_female"))
    builder.add(InlineKeyboardButton(text="Любой", callback_data="gender_any"))
    builder.add(InlineKeyboardButton(text="Назад к фильтрам", callback_data="back_to_filters"))
    builder.adjust(2, 1, 1)
    return builder.as_markup()


# Фильтр по возрасту
def age_filter_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Котенок (до 1 года)", callback_data="age_kitten"))
    builder.add(InlineKeyboardButton(text="Молодой (1-3 года)", callback_data="age_young"))
    builder.add(InlineKeyboardButton(text="Взрослый (4-7 лет)", callback_data="age_adult"))
    builder.add(InlineKeyboardButton(text="Пожилой (8+ лет)", callback_data="age_senior"))
    builder.add(InlineKeyboardButton(text="Любой возраст", callback_data="age_any"))
    builder.add(InlineKeyboardButton(text="Назад к фильтрам", callback_data="back_to_filters"))
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


# Фильтр по дружелюбности
def temperament_filter_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Дружелюбный к детям", callback_data="temperament_kids"))
    builder.add(InlineKeyboardButton(text="Дружелюбный к животным", callback_data="temperament_pets"))
    builder.add(InlineKeyboardButton(text="Любой характер", callback_data="temperament_any"))
    builder.add(InlineKeyboardButton(text="Назад к фильтрам", callback_data="back_to_filters"))
    builder.adjust(2, 1, 1)
    return builder.as_markup()


# Навигация по котам
def cats_navigation(current_index: int, total_cats: int, cat_id: int):
    builder = InlineKeyboardBuilder()

    if current_index > 0:
        builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"cat_{current_index - 1}"))

    builder.add(InlineKeyboardButton(text="🏠 Приютить", callback_data=f"adopt_{cat_id}"))

    if current_index < total_cats - 1:
        builder.add(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"cat_{current_index + 1}"))

    builder.add(InlineKeyboardButton(text="🔙 Назад к фильтрам", callback_data="back_to_filters"))
    builder.adjust(3, 1)
    return builder.as_markup()


# Кнопка для приюта
def adoption_menu(cat_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Подтвердить приют", callback_data=f"confirm_adopt_{cat_id}"))
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_adoption"))
    builder.adjust(1, 1)
    return builder.as_markup()


# Кнопка локации
def location_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📍 Открыть в Google Maps", url="https://maps.google.com"))
    builder.add(InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu"))
    builder.adjust(1, 1)
    return builder.as_markup()


# Кнопка сайта
def website_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://ваше-котокафе.ру"))
    builder.add(InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu"))
    builder.adjust(1, 1)
    return builder.as_markup()


# Кнопка назад в главное меню
def back_to_main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu"))
    return builder.as_markup()