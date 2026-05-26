from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="✨ Начать сонастройку", callback_data="start_flow"))
    return builder.as_markup()

def get_spheres_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="💼 Карьера / Финансы", callback_data="sphere:finance"))
    builder.add(types.InlineKeyboardButton(text="❤️ Отношения", callback_data="sphere:relations"))
    builder.add(types.InlineKeyboardButton(text="🍏 Здоровье / Энергия", callback_data="sphere:health"))
    builder.add(types.InlineKeyboardButton(text="🧘‍♂️ Внутренний баланс", callback_data="sphere:mind"))
    builder.adjust(1)
    return builder.as_markup()

def get_end_session_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="✨ Новая сонастройка", callback_data="restart_flow"))
    builder.add(types.InlineKeyboardButton(text="🔄 Полный перезапуск бота", callback_data="full_restart"))
    builder.adjust(1) # Размещает кнопки строго друг под другом
    return builder.as_markup()

def get_settings_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="📬 Мягкая доставка (без звука)", callback_data="set_mode:soft"))
    builder.add(types.InlineKeyboardButton(text="⏰ Точное время (со звуком)", callback_data="set_mode:exact"))
    builder.add(types.InlineKeyboardButton(text="🧘‍♂️ Ручной запуск (оставить всё как есть)", callback_data="set_mode:manual"))
    builder.adjust(1)
    return builder.as_markup()

# Словарь для перевода ключей в красивый текст
SPHERES_RU = {
    "finance": "💼 Карьера и Финансы",
    "relations": "❤️ Отношения и Семья",
    "health": "🍏 Здоровье и Энергия",
    "mind": "🧘‍♂️ Внутренний баланс и Покой"
}