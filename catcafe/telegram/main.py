import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import config
import keyboard

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Базовый URL для API (замените на ваш реальный URL)
API_BASE_URL = "https://localhost:8000/api"

# Инициализация бота и диспетчера
bot = Bot(token=config.botkey)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Состояния FSM
class CatFilters(StatesGroup):
    choosing_filters = State()
    viewing_cats = State()


# Глобальные переменные для хранения состояния
user_states = {}
filtered_cats = {}


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🐱 Добро пожаловать в котокафе-приют!\n\n"
        "Здесь вы можете:\n"
        "• Посмотреть наших замечательных котов\n"
        "• Приютить понравившегося котика\n"
        "• Узнать где мы находимся\n"
        "• Посетить наш сайт\n\n"
        "Выберите действие в меню ниже:",
        reply_markup=keyboard.main_menu()
    )


# Обработка текстовых сообщений
@dp.message(F.text == "🐱 Посмотреть котов")
async def show_cats(message: Message, state: FSMContext):
    await state.set_state(CatFilters.choosing_filters)
    await message.answer(
        "🔍 Выберите фильтры для поиска котов:",
        reply_markup=keyboard.cats_filter_menu()
    )


@dp.message(F.text == "🏠 Приютить кота")
async def adopt_info(message: Message):
    await message.answer(
        "Чтобы приютить кота, сначала посмотрите наших питомцев через меню '🐱 Посмотреть котов' "
        "и выберите понравившегося!"
    )


@dp.message(F.text == "📍 Локация приюта")
async def show_location(message: Message):
    await message.answer(
        "📍 Наш приют находится по адресу:\n"
        "г. Москва, ул. Котофея, д. 15\n\n"
        "Часы работы: 10:00 - 22:00",
        reply_markup=keyboard.location_menu()
    )


@dp.message(F.text == "🌐 Сайт котокафе")
async def show_website(message: Message):
    await message.answer(
        "🌐 Посетите наш сайт, чтобы узнать больше о котокафе, меню, событиях и акциях!",
        reply_markup=keyboard.website_menu()
    )


# Обработка callback запросов для фильтров
@dp.callback_query(F.data == "filter_gender")
async def filter_gender(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите пол кота:",
        reply_markup=keyboard.gender_filter_menu()
    )


@dp.callback_query(F.data == "filter_age")
async def filter_age(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите возраст:",
        reply_markup=keyboard.age_filter_menu()
    )


@dp.callback_query(F.data == "filter_temperament")
async def filter_temperament(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите дружелюбность:",
        reply_markup=keyboard.temperament_filter_menu()
    )


@dp.callback_query(F.data == "back_to_filters")
async def back_to_filters(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CatFilters.choosing_filters)
    await callback.message.edit_text(
        "🔍 Выберите фильтры для поиска котов:",
        reply_markup=keyboard.cats_filter_menu()
    )


# Обработка выбора пола
@dp.callback_query(F.data.startswith("gender_"))
async def set_gender_filter(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    gender_map = {
        "gender_male": "male",
        "gender_female": "female",
        "gender_any": "any"
    }

    if user_id not in user_states:
        user_states[user_id] = {}
    user_states[user_id]['gender'] = gender_map[callback.data]

    await callback.message.edit_text(
        "Пол выбран! Выберите другие фильтры или нажмите 'Показать всех котов'",
        reply_markup=keyboard.cats_filter_menu()
    )


# Обработка выбора возраста
@dp.callback_query(F.data.startswith("age_"))
async def set_age_filter(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    age_map = {
        "age_kitten": "kitten",
        "age_young": "young",
        "age_adult": "adult",
        "age_senior": "senior",
        "age_any": "any"
    }

    if user_id not in user_states:
        user_states[user_id] = {}
    user_states[user_id]['age'] = age_map[callback.data]

    await callback.message.edit_text(
        "Возраст выбран! Выберите другие фильтры или нажмите 'Показать всех котов'",
        reply_markup=keyboard.cats_filter_menu()
    )


# Обработка дружелюбности
@dp.callback_query(F.data.startswith("temperament_"))
async def set_temperament_filter(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    temp_map = {
        "temperament_kids": "friendly_kids",
        "temperament_pets": "friendly_pets",
        "temperament_any": "any"
    }

    if user_id not in user_states:
        user_states[user_id] = {}
    user_states[user_id]['temperament'] = temp_map[callback.data]

    await callback.message.edit_text(
        "Дружелюбность выбрана! Выберите другие фильтры или нажмите 'Показать всех котов'",
        reply_markup=keyboard.cats_filter_menu()
    )


# Получить котов из API
async def get_cats_from_api(filters=None):
    try:
        url = f"{API_BASE_URL}/cats/"
        params = {}

        if filters:
            if filters.get('gender') and filters['gender'] != 'any':
                params['gender'] = filters['gender']
            if filters.get('age') and filters['age'] != 'any':
                params['age'] = filters['age']
            if filters.get('temperament') and filters['temperament'] != 'any':
                params['temperament'] = filters['temperament']

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.error(f"Ошибка при получении данных из API: {e}")
        return []


# Показать котов
@dp.callback_query(F.data == "show_all_cats")
async def show_all_cats(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    filters = user_states.get(user_id, {})

    await callback.message.edit_text("🔍 Ищем котов по вашим фильтрам...")

    cats = await get_cats_from_api(filters)

    if not cats:
        await callback.message.edit_text(
            "😿 К сожалению, по вашим фильтрам котов не найдено.\n"
            "Попробуйте изменить критерии поиска.",
            reply_markup=keyboard.cats_filter_menu()
        )
        return

    filtered_cats[user_id] = cats
    await state.set_state(CatFilters.viewing_cats)
    await show_cat(callback, user_id, 0)


# Навигация по котам
@dp.callback_query(F.data.startswith("cat_"))
async def navigate_cats(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    index = int(callback.data.split("_")[1])
    await show_cat(callback, user_id, index)


# Показать информацию о коте
async def show_cat(callback: CallbackQuery, user_id: int, index: int):
    cats = filtered_cats.get(user_id, [])

    if not cats or index >= len(cats):
        await callback.message.edit_text(
            "Коты не найдены",
            reply_markup=keyboard.cats_filter_menu()
        )
        return

    cat = cats[index]
    message = format_cat_info(cat, index, len(cats))

    # Если есть фото, отправляем его
    if cat.get('photo'):
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=cat['photo'],
                caption=message,
                reply_markup=keyboard.cats_navigation(index, len(cats), cat['id'])
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке фото: {e}")
            await callback.message.edit_text(
                message,
                reply_markup=keyboard.cats_navigation(index, len(cats), cat['id'])
            )
    else:
        await callback.message.edit_text(
            message,
            reply_markup=keyboard.cats_navigation(index, len(cats), cat['id'])
        )


# Форматирование информации о коте
def format_cat_info(cat, current_index, total_cats):
    gender_emoji = "♂️" if cat.get('gender') == 'male' else "♀️"
    age_text = get_age_text(cat.get('age'))

    message = f"🐱 <b>{cat.get('name', 'Без имени')}</b> {gender_emoji}\n\n"
    message += f"<b>Порода:</b> {cat.get('breed', 'Не указана')}\n"
    message += f"<b>Возраст:</b> {age_text}\n"
    message += f"<b>Характер:</b> {cat.get('temperament', 'Не указан')}\n"
    message += f"<b>Статус:</b> {cat.get('status', 'Не указан')}\n\n"

    if cat.get('description'):
        message += f"<i>{cat.get('description')}</i>\n\n"

    message += f"📄 {current_index + 1}/{total_cats}"

    return message


# Получить текстовое описание возраста
def get_age_text(age):
    age_map = {
        'kitten': 'Котенок (до 1 года)',
        'young': 'Молодой (1-3 года)',
        'adult': 'Взрослый (4-7 лет)',
        'senior': 'Пожилой (8+ лет)'
    }
    return age_map.get(age, 'Не указан')


# Приют кота
@dp.callback_query(F.data.startswith("adopt_"))
async def adopt_cat(callback: CallbackQuery):
    cat_id = callback.data.split("_")[1]
    await callback.message.edit_text(
        "🏠 Вы уверены, что хотите приютить этого кота?\n\n"
        "После подтверждения с вами свяжется наш менеджер для оформления документов.",
        reply_markup=keyboard.adoption_menu(cat_id)
    )


# Подтверждение приюта
@dp.callback_query(F.data.startswith("confirm_adopt_"))
async def confirm_adoption(callback: CallbackQuery, state: FSMContext):
    cat_id = callback.data.split("_")[2]

    # Здесь можно добавить логику сохранения заявки на приют
    # и отправки уведомления администратору

    await callback.message.edit_text(
        "✅ Заявка на приют отправлена!\n\n"
        "Наш менеджер свяжется с вами в ближайшее время для уточнения деталей.\n\n"
        "Спасибо, что даете коту новый дом! 🐱❤️"
    )

    # Уведомление администратору
    try:
        await bot.send_message(
            config.admin,
            f"📋 Новая заявка на приют!\n"
            f"От: {callback.from_user.full_name} (@{callback.from_user.username})\n"
            f"ID пользователя: {callback.from_user.id}\n"
            f"ID кота: {cat_id}"
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления администратору: {e}")


# Отмена приюта
@dp.callback_query(F.data == "cancel_adoption")
async def cancel_adoption(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CatFilters.choosing_filters)
    await callback.message.edit_text(
        "🔍 Выберите фильтры для поиска котов:",
        reply_markup=keyboard.cats_filter_menu()
    )


# Возврат в главное меню
@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Возвращаемся в главное меню:",
        reply_markup=keyboard.main_menu()
    )


# Обработка неизвестных сообщений
@dp.message()
async def handle_unknown(message: Message):
    await message.answer(
        "Используйте кнопки меню для навигации",
        reply_markup=keyboard.main_menu()
    )


# Основная функция
async def main():
    logger.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())