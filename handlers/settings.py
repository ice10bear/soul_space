import re
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states import SoulSpaceStates
from keyboards import get_settings_keyboard
import database

router = Router()

# Команда /settings для вызова меню настроек времени
@router.message(F.text == "/settings")
async def cmd_settings(message: types.Message, state: FSMContext):
    await state.clear()
    current_settings = database.get_user_settings(message.from_user.id)
    
    modes_ru = {
        "manual": "🧘‍♂️ Ручной запуск",
        "soft": "📬 Мягкая доставка (без звука)",
        "exact": "⏰ Точное время (со звуком)"
    }
    
    current_text = f"Текущий режим: *{modes_ru.get(current_settings['mode'])}*\n"
    if current_settings['time']:
        current_text += f"Установленное время: *{current_settings['time']}*\n\n"
    else:
        current_text += "\n"
        
    await message.answer(
        f"{current_text}✨ **Настройка утреннего пространства**\n\n"
        "Выберите, как Наставнику бережнее сонастраиваться с Вашим ритмом дня:",
        reply_markup=get_settings_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(SoulSpaceStates.setting_mode)

@router.callback_query(F.data.startswith("set_mode:"), SoulSpaceStates.setting_mode)
async def process_mode_choice(callback: types.CallbackQuery, state: FSMContext):
    mode = callback.data.split(":")[1]
    await callback.answer()
    
    if mode == "manual":
        database.save_user_settings(callback.from_user.id, "manual", None)
        await callback.message.edit_text(
            "✨ Настройки сохранены. Вы оставили **Ручной запуск**.\n"
            "Наставник будет ждать Вас в SoulSpace в любое время, когда Вы сами откроете бот.",
            parse_mode="Markdown"
        )
        await state.clear()
    else:
        # Если выбрали мягкую или точную доставку — запрашиваем время
        await state.update_data(chosen_mode=mode)
        mode_text = "беззвучной" if mode == "soft" else "звуковой"
        await callback.message.edit_text(
            f"Вы выбрали режим для **{mode_text}** доставки.\n\n"
            "Укажите желаемое время в формате **ЧЧ:ММ** (например, `07:30` или `09:15`):",
            parse_mode="Markdown"
        )
        await state.set_state(SoulSpaceStates.waiting_for_time)

@router.message(SoulSpaceStates.waiting_for_time)
async def process_time_input(message: types.Message, state: FSMContext):
    time_input = message.text.strip()
    
    # Проверка формата времени через регулярное выражение (HH:MM)
    if not re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", time_input):
        await message.answer("Пожалуйста, введите время в правильном формате **ЧЧ:ММ** (например, `08:00`).")
        return
        
    user_data = await state.get_data()
    mode = user_data.get("chosen_mode")
    
    # Сохраняем в базу данных
    database.save_user_settings(message.from_user.id, mode, time_input)
    
    mode_final = "📬 Мягкая доставка (без звука)" if mode == "soft" else "⏰ Точное время (со звуком)"
    
    await message.answer(
        f"✨ **Настройки успешно применены!**\n\n"
        f"Режим: *{mode_final}*\n"
        f"Время встречи: *{time_input}*\n\n"
        "Каждое утро Наставник будет бережно ожидать Вас.",
        parse_mode="Markdown"
    )
    await state.clear()