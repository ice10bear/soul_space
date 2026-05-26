from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import get_start_keyboard, get_spheres_keyboard, get_mini_app_keyboard, SPHERES_RU
from states import SoulSpaceStates

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        "Приветствуем в **SoulSpace**. ✨\n\n"
        "Это пространство Вашего утреннего спокойствия и бережной настройки на день. "
        "Здесь не нужно спешить. Сделайте глубокий вдох, выдохните прошлый день и, "
        "когда будете готовы, давайте начнем."
    )
    # Сразу открываем Mini App для пользователя по команде /start
    await message.answer(welcome_text, reply_markup=get_mini_app_keyboard(), parse_mode="Markdown")


@router.callback_query(F.data == "start_flow")
async def start_flow_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    choose_text = (
        "Я Ваш цифровой наставник.\n\n"
        "Чтобы сегодняшняя практика прошла точнее, **выберите сферу жизни**, "
        "которая сейчас требует Вашего наибольшего внимания или поддержки:"
    )
    await callback.message.edit_text(choose_text, reply_markup=get_spheres_keyboard(), parse_mode="Markdown")
    await state.set_state(SoulSpaceStates.choosing_sphere)


@router.callback_query(F.data == "restart_flow")
async def restart_flow_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear() 
    
    choose_text = (
        "Рад нашей новой сонастройке. ✨\n\n"
        "Выберите сферу жизни, которая сейчас требует Вашего наибольшего внимания:"
    )
    await callback.message.answer(choose_text, reply_markup=get_spheres_keyboard(), parse_mode="Markdown")
    await state.set_state(SoulSpaceStates.choosing_sphere)


# =====================================================================
# НАШ ОБНОВЛЕННЫЙ МОСТИК ДЛЯ ОБРАБОТКИ ВЫБОРА СФЕРЫ (С УЧЕТОМ КЛЮЧЕЙ GROQ)
# =====================================================================
@router.callback_query(SoulSpaceStates.choosing_sphere)
async def sphere_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Извлекаем ключ сферы (например, из "sphere:finance" берем "finance")
    sphere_key = callback.data.split(":")[-1] if ":" in callback.data else callback.data
    
    # Берем красивое название из твоего словаря SPHERES_RU или оставляем как есть
    chosen_sphere = SPHERES_RU.get(sphere_key, "Внутренний баланс и Покой")

    # Сохраняем сферу в память FSM
    await state.update_data(chosen_sphere=chosen_sphere)
    
    # Переключаем состояние на ожидание текста настроения
    await state.set_state(SoulSpaceStates.waiting_for_mood)
    
    prompt_text = (
        f"Вы выбрали сферу: **{chosen_sphere}**. ✨\n\n"
        "Пожалуйста, опишите парой предложений ваше текущее состояние, мысли или настроение. "
        "Что Вас сейчас волнует? Наставник выслушает Вас..."
    )
    # Меняем текст сообщения, предлагая пользователю написать ответ в чат
    await callback.message.edit_text(prompt_text, parse_mode="Markdown")


@router.callback_query(F.data == "full_restart")
async def full_restart_chosen(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    
    welcome_text = (
        "Приветствуем в **SoulSpace**. ✨\n\n"
        "Это пространство Вашего утреннего спокойствия и бережной настройки на день. "
        "Когда будете готовы, давайте начнем с самого начала."
    )
    # При полном перезапуске тоже даем кнопку вызова Mini App
    await callback.message.answer(welcome_text, reply_markup=get_mini_app_keyboard(), parse_mode="Markdown")