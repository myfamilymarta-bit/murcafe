import asyncio
import aiohttp
import csv
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import keyboard
import config

bot = Bot(token=config.botkey)
dp = Dispatcher()

ADOPTIONS_CSV = "adoptions.csv"

def init_adoptions_csv():
    if not os.path.exists(ADOPTIONS_CSV):
        with open(ADOPTIONS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['cat_id', 'cat_name', 'user_id', 'username', 'full_name', 'timestamp', 'status'])


def save_adoption(cat_id: int, cat_name: str, user_id: int, username: str, status='reserved'):
    full_name = username
    with open(ADOPTIONS_CSV, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            cat_id,
            cat_name,
            user_id,
            username,
            full_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status
        ])


def get_reserved_cats():
    reserved_cats = []
    if not os.path.exists(ADOPTIONS_CSV):
        return reserved_cats

    try:
        with open(ADOPTIONS_CSV, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row or not row.get('cat_id'):
                    continue

                cat_id = row.get('cat_id', '').strip()
                status = row.get('status', '').strip()

                if cat_id.isdigit() and status == 'reserved':
                    reserved_cats.append(row)
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")

    return reserved_cats


def get_all_adopted_cats():
    adopted_cats = set()
    if os.path.exists(ADOPTIONS_CSV):
        try:
            with open(ADOPTIONS_CSV, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    adopted_cats.add(int(row['cat_id']))
        except Exception as e:
            print(f"Ошибка при чтении adopted cats: {e}")
    return adopted_cats


def update_adoption_status(cat_id: int, new_status: str):
    temp_file = ADOPTIONS_CSV + '.tmp'
    updated = False

    try:
        with open(ADOPTIONS_CSV, 'r', encoding='utf-8') as file, open(temp_file, 'w', newline='',
                                                                      encoding='utf-8') as out_file:
            reader = csv.DictReader(file)
            writer = csv.writer(out_file)
            writer.writerow(['cat_id', 'cat_name', 'user_id', 'username', 'full_name', 'timestamp', 'status'])

            for row in reader:
                if not row or not row.get('cat_id'):
                    continue

                current_cat_id = row['cat_id'].strip()
                print(
                    f"Сравниваем: текущий ID '{current_cat_id}' (тип: {type(current_cat_id)}), ищем ID {cat_id} (тип: {type(cat_id)})")

                if current_cat_id.isdigit() and int(current_cat_id) == cat_id:
                    print(f"Найдена запись для обновления: кот {cat_id}")
                    writer.writerow([
                        row['cat_id'],
                        row['cat_name'],
                        row['user_id'],
                        row['username'],
                        row['full_name'],
                        row['timestamp'],
                        new_status
                    ])
                    updated = True
                else:
                    writer.writerow([
                        row['cat_id'],
                        row['cat_name'],
                        row['user_id'],
                        row['username'],
                        row['full_name'],
                        row['timestamp'],
                        row.get('status', 'reserved')
                    ])

        if updated:
            os.replace(temp_file, ADOPTIONS_CSV)
            print(f"Файл обновлен успешно, статус кота {cat_id} изменен на {new_status}")
        else:
            print(f"Запись для кота {cat_id} не найдена")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except Exception as e:
        print(f"Ошибка при обновлении статуса: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return updated


def remove_adoption(cat_id: int):
    temp_file = ADOPTIONS_CSV + '.tmp'
    rows_kept = 0
    removed = False

    try:
        with open(ADOPTIONS_CSV, 'r', encoding='utf-8') as file, open(temp_file, 'w', newline='',
                                                                      encoding='utf-8') as out_file:
            reader = csv.DictReader(file)
            writer = csv.writer(out_file)
            writer.writerow(['cat_id', 'cat_name', 'user_id', 'username', 'full_name', 'timestamp', 'status'])

            for row in reader:
                if not row or not row.get('cat_id'):
                    continue

                current_cat_id = row['cat_id'].strip()
                if current_cat_id.isdigit() and int(current_cat_id) == cat_id:
                    print(f"Удалена запись для кота {cat_id}")
                    removed = True
                else:
                    writer.writerow([
                        row['cat_id'],
                        row['cat_name'],
                        row['user_id'],
                        row['username'],
                        row['full_name'],
                        row['timestamp'],
                        row.get('status', 'reserved')
                    ])
                    rows_kept += 1

        if removed:
            os.replace(temp_file, ADOPTIONS_CSV)
            print(f"Удаление завершено, сохранено строк: {rows_kept}")
        else:
            print(f"Запись для удаления кота {cat_id} не найдена")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return removed


async def get_cats_from_api():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/api/cats/') as response:
                if response.status == 200:
                    cats = await response.json()
                    return cats
                else:
                    print(f"API error: {response.status}")
                    return []
    except Exception as e:
        print(f"Error fetching cats: {e}")
        return []

async def get_available_cats():
    all_cats = await get_cats_from_api()
    adopted_cats = get_all_adopted_cats()

    available_cats = []
    for cat in all_cats:
        if cat.get('status') == 'available' and cat.get('id') not in adopted_cats:
            available_cats.append(cat)

    print(f"Доступных котов: {len(available_cats)}, всего котов: {len(all_cats)}, усыновленных: {len(adopted_cats)}")
    return available_cats


def format_cat_info(cat: dict, index: int, total: int):
    gender_emoji = "♂️" if cat.get('gender') == 'M' else "♀️"

    age_mapping = {
        'kitten': 'Котенок (до 1 года)',
        'young': 'Молодой (1-3 года)',
        'adult': 'Взрослый (3-8 лет)',
        'senior': 'Пожилой (8+ лет)'
    }

    temperament_map = {
        'active': 'Активный',
        'calm': 'Спокойный',
        'playful': 'Игривый',
        'affectionate': 'Ласковый',
        'shy': 'Стеснительный',
        'lazy': 'Ленивый'
    }

    temperament = temperament_map.get(cat.get('temperament', ''), cat.get('temperament', ''))
    age = age_mapping.get(cat.get('age', ''), cat.get('age', 'Не указан'))

    cat_name = cat.get("name", "Без имени")
    breed = cat.get('breed', 'Не указана')
    description = cat.get('description', 'Нет описания')
    story = cat.get('story', '')
    health_status = cat.get('health_status', 'Не указано')
    special_needs = cat.get('special_needs', '')

    text = f"🐱 {cat_name} {gender_emoji}\n\n"
    text += f"📍 Статус: Ищет дом\n"
    text += f"🎂 Возраст: {age}\n"
    text += f"🐾 Порода: {breed}\n"
    text += f"💫 Характер: {temperament}\n\n"
    text += f"📖 Описание:\n{description}\n\n"

    if story:
        text += f"📚 История:\n{story}\n\n"
    text += f"🏥 Здоровье:\n"
    text += f"• {health_status}\n"
    if cat.get('vaccinated'):
        text += "• Привит\n"
    if cat.get('sterilized'):
        text += "• Стерилизован\n"
    if special_needs:
        text += f"• Особые потребности: {special_needs}\n"

    text += f"\n📄 {index + 1}/{total}"

    return text


def format_reserved_cat_info(cat_data: dict, index: int, total: int):
    text = f"🐱 {cat_data['cat_name']}\n\n"
    text += f"📍 Статус: 🔄 Зарезервирован\n"
    text += f"🆔 ID кота: {cat_data['cat_id']}\n\n"

    text += f"📋 Информация о резервации:\n"
    text += f"• Пользователь: {cat_data.get('username', 'Не указан')}\n"
    text += f"• ID пользователя: {cat_data.get('user_id', 'Не указан')}\n"
    text += f"• Полное имя: {cat_data.get('full_name', 'Не указано')}\n"
    text += f"• Дата резервации: {cat_data.get('timestamp', 'Не указана')}\n\n"

    text += f"📄 {index + 1}/{total}\n\n"
    text += "Выберите действие для этого кота:"

    return text

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "🐱 Добро пожаловать в приют для котиков! 🐱\n\n"
        "Здесь вы можете:\n"
        "• Посмотреть котиков, ищущих дом\n"
        "• Узнать как приютить кота\n"
        "• Найти наш приют\n\n"
        "Выберите действие:"
    )

    if message.from_user.id == config.admin:
        await message.answer(welcome_text, reply_markup=keyboard.admin_main_menu())
    else:
        await message.answer(welcome_text, reply_markup=keyboard.main_menu())


@dp.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    welcome_text = (
        "🐱 Добро пожаловать в приют для котиков! 🐱\n\n"
        "Выберите действие:"
    )
    if callback.from_user.id == config.admin:
        await callback.message.edit_text(welcome_text, reply_markup=keyboard.admin_main_menu())
    else:
        await callback.message.edit_text(welcome_text, reply_markup=keyboard.main_menu())
    await callback.answer()


@dp.callback_query(F.data == "view_cats")
async def view_cats(callback: CallbackQuery):
    await callback.answer("Загружаем котиков...")

    cats = await get_available_cats()

    if not cats:
        await callback.message.edit_text(
            "😿 Пока нет доступных котиков для усыновления. Попробуйте позже!",
            reply_markup=keyboard.main_menu()
        )
        return

    cat = cats[0]
    text = format_cat_info(cat, 0, len(cats))

    is_admin = callback.from_user.id == config.admin
    if is_admin:
        markup = keyboard.admin_cats_navigation(0, len(cats), cat['id'])
    else:
        markup = keyboard.cats_navigation(0, len(cats), cat['id'])

    await callback.message.edit_text(text, reply_markup=markup)


@dp.callback_query(F.data == "view_reserved")
async def view_reserved_cats(callback: CallbackQuery):
    if callback.from_user.id != config.admin:
        await callback.answer("У вас нет прав для этого действия")
        return

    await callback.answer("Загружаем зарезервированных котиков...")
    cats = get_reserved_cats()
    print(f"Найдено зарезервированных котов: {len(cats)}")

    if not cats:
        await callback.message.edit_text(
            "📋 Нет зарезервированных котиков.",
            reply_markup=keyboard.admin_main_menu()
        )
        return

    cat = cats[0]
    text = format_reserved_cat_info(cat, 0, len(cats))

    markup = keyboard.reserved_cats_navigation(0, len(cats), int(cat['cat_id']))
    await callback.message.edit_text(text, reply_markup=markup)


@dp.callback_query(F.data.startswith("cat_"))
async def navigate_cats(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    cats = await get_available_cats()

    if not cats or index >= len(cats):
        await callback.answer("Котик не найден")
        return

    cat = cats[index]
    text = format_cat_info(cat, index, len(cats))

    is_admin = callback.from_user.id == config.admin
    if is_admin:
        markup = keyboard.admin_cats_navigation(index, len(cats), cat['id'])
    else:
        markup = keyboard.cats_navigation(index, len(cats), cat['id'])

    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data.startswith("reserved_cat_"))
async def navigate_reserved_cats(callback: CallbackQuery):
    if callback.from_user.id != config.admin:
        await callback.answer("У вас нет прав для этого действия")
        return

    index = int(callback.data.split("_")[2])
    cats = get_reserved_cats()

    if not cats or index >= len(cats):
        await callback.answer("Котик не найден")
        return

    cat = cats[index]
    text = format_reserved_cat_info(cat, index, len(cats))

    markup = keyboard.reserved_cats_navigation(index, len(cats), int(cat['cat_id']))
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data == "adoption_info")
async def adoption_info(callback: CallbackQuery):
    info_text = (
        "🏠 Как приютить кота:\n\n"
        "1. Посмотрите доступных котиков через кнопку '🐱 Посмотреть котов'\n"
        "2. Выберите понравившегося котика\n"
        "3. Нажмите кнопку '🏠 Приютить кота'\n"
        "4. Подтвердите свое решение\n\n"
        "После этого с вами свяжется наш менеджер для уточнения деталей.\n\n"
        "📞 Контакты:\n"
        "Телефон: +375 (33) 123-45-67\n"
        "Email: shelter_cats@gmail.com\n\n"
        "Мы работаем ежедневно с 10:00 до 20:00"
    )

    builder = keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🐱 Посмотреть котов", callback_data="view_cats"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"))

    await callback.message.edit_text(info_text, reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data == "shelter_location")
async def shelter_location(callback: CallbackQuery):
    location_text = (
        "📍 Наш приют находится по адресу:\n\n"
        "🏠 Улица Кошачья, дом 15\n"
        "Минск, Беларусь\n\n"
        "🚇 Ближайшее метро: Котиковская\n"
        "🕒 Часы работы: 10:00 - 22:00 ежедневно"
    )

    await callback.message.edit_text(location_text, reply_markup=keyboard.location_menu())
    await callback.answer()


@dp.callback_query(F.data.startswith("adopt_"))
async def start_adoption(callback: CallbackQuery):
    cat_id = int(callback.data.split("_")[1])
    cats = await get_available_cats()
    current_cat = None
    for cat in cats:
        if cat['id'] == cat_id:
            current_cat = cat
            break

    if not current_cat:
        await callback.answer("Котик не найден или уже приючен")
        return

    cat_name = current_cat['name']
    adoption_text = (
        f"🐱 Вы хотите приютить {cat_name}?\n\n"
        "После подтверждения:\n"
        "• Котик будет зарезервирован за вами\n"
        "• С вами свяжется наш менеджер\n"
        "• Вы сможете забрать котика в удобное время\n\n"
        "✅ Подтвердите усыновление:"
    )

    await callback.message.edit_text(adoption_text, reply_markup=keyboard.adoption_menu(cat_id))
    await callback.answer()


@dp.callback_query(F.data.startswith("confirm_adopt_"))
async def confirm_adoption(callback: CallbackQuery):
    cat_id = int(callback.data.split("_")[2])
    cats = await get_available_cats()

    current_cat = None
    for cat in cats:
        if cat['id'] == cat_id:
            current_cat = cat
            break

    if not current_cat:
        await callback.answer("Котик не найден или уже приючен")
        return
    username = callback.from_user.username or callback.from_user.first_name
    save_adoption(cat_id, current_cat['name'], callback.from_user.id, username, 'reserved')

    cat_name = current_cat['name']
    success_text = (
        f"🎉 Поздравляем! Вы приютили {cat_name}!\n\n"
        "📞 Наш менеджер свяжется с вами в течение 24 часов "
        "для уточнения деталей.\n\n"
        "Спасибо, что даете дом бездомному котику! 💕"
    )

    builder = keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🐱 Посмотреть других котов", callback_data="view_cats"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"))

    await callback.message.edit_text(success_text, reply_markup=builder.as_markup())
    await callback.answer(f"Вы приютили {cat_name}!")


@dp.callback_query(F.data.startswith("confirm_adopted_"))
async def confirm_adopted(callback: CallbackQuery):
    if callback.from_user.id != config.admin:
        await callback.answer("У вас нет прав для этого действия")
        return

    cat_id = int(callback.data.split("_")[2])
    print(f"Подтверждение усыновления для кота {cat_id}")
    success = update_adoption_status(cat_id, 'adopted')

    if success:
        await callback.answer("✅ Статус изменен на 'Усыновлен'")
        await view_reserved_cats(callback)
    else:
        await callback.answer("❌ Ошибка при изменении статуса")


@dp.callback_query(F.data.startswith("cancel_reservation_"))
async def cancel_reservation(callback: CallbackQuery):
    if callback.from_user.id != config.admin:
        await callback.answer("У вас нет прав для этого действия")
        return

    cat_id = int(callback.data.split("_")[2])
    print(f"Отмена резервации для кота {cat_id}")
    success = remove_adoption(cat_id)

    if success:
        await callback.answer("❌ Резервация отменена")
        await view_reserved_cats(callback)
    else:
        await callback.answer("❌ Ошибка при отмене резервации")


@dp.callback_query(F.data == "back_to_cats")
async def back_to_cats(callback: CallbackQuery):
    await view_cats(callback)


@dp.message()
async def unknown_message(message: Message):
    await message.answer(
        "Пожалуйста, используйте кнопки меню для навигации",
        reply_markup=keyboard.main_menu()
    )

async def main():
    init_adoptions_csv()
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())