from aiogram.fsm.state import StatesGroup, State

class SoulSpaceStates(StatesGroup):
    choosing_sphere = State()   # Ожидание выбора сферы
    waiting_for_mood = State()  # Ожидание текста настроения
    
    # Новые состояния для настроек времени:
    setting_mode = State()      # Выбор режима доставки
    waiting_for_time = State()  # Ожидание ввода времени (например, "08:30")