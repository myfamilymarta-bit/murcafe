from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🐱 Посмотреть котов", callback_data="view_cats"))
    builder.row(types.InlineKeyboardButton(text="🏠 Приютить кота", callback_data="adoption_info"))
    builder.row(types.InlineKeyboardButton(text="📍 Локация приюта", callback_data="shelter_location"))
    return builder.as_markup()

def admin_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🐱 Посмотреть котов", callback_data="view_cats"))
    builder.row(types.InlineKeyboardButton(text="📋 Зарезервированные коты", callback_data="view_reserved"))
    builder.row(types.InlineKeyboardButton(text="🏠 Приютить кота", callback_data="adoption_info"))
    builder.row(types.InlineKeyboardButton(text="📍 Локация приюта", callback_data="shelter_location"))
    return builder.as_markup()

def cats_navigation(current_index: int, total_cats: int, cat_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(types.InlineKeyboardButton(text="🏠 Приютить кота", callback_data=f"adopt_{cat_id}"))

    buttons = []
    if current_index > 0:
        buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"cat_{current_index - 1}"))

    buttons.append(types.InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"))

    if current_index < total_cats - 1:
        buttons.append(types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"cat_{current_index + 1}"))

    if buttons:
        builder.row(*buttons)

    return builder.as_markup()

def admin_cats_navigation(current_index: int, total_cats: int, cat_id: int, is_adopted: bool = False):
    builder = InlineKeyboardBuilder()

    if is_adopted:
        builder.row(types.InlineKeyboardButton(text="❌ Отменить усыновление", callback_data=f"unadopt_{cat_id}"))
    else:
        builder.row(types.InlineKeyboardButton(text="🏠 Приютить кота", callback_data=f"adopt_{cat_id}"))

    buttons = []
    if current_index > 0:
        buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"cat_{current_index - 1}"))

    buttons.append(types.InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"))

    if current_index < total_cats - 1:
        buttons.append(types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"cat_{current_index + 1}"))

    if buttons:
        builder.row(*buttons)

    return builder.as_markup()

def reserved_cats_navigation(current_index: int, total_cats: int, cat_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(types.InlineKeyboardButton(text="✅ Подтвердить усыновление", callback_data=f"confirm_adopted_{cat_id}"))
    builder.row(types.InlineKeyboardButton(text="❌ Отменить резервацию", callback_data=f"cancel_reservation_{cat_id}"))

    buttons = []
    if current_index > 0:
        buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"reserved_cat_{current_index - 1}"))

    buttons.append(types.InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"))

    if current_index < total_cats - 1:
        buttons.append(types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"reserved_cat_{current_index + 1}"))

    if buttons:
        builder.row(*buttons)

    return builder.as_markup()

def adoption_menu(cat_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Да, хочу приютить!", callback_data=f"confirm_adopt_{cat_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к котам", callback_data="back_to_cats"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    return builder.as_markup()

def location_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📍 Открыть в картах", url="https://yandex.ru/maps/"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    return builder.as_markup()
