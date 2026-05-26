from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot, dp
from keyboards import get_spheres_keyboard
from states import SoulSpaceStates
import database

async def check_morning_delivery():
    # Получаем текущее время в формате ЧЧ:ММ (например, "07:30")
    current_time = datetime.now().strftime("%H:%M")
    
    # Ищем в базе тех, кому пора отправлять
    users_to_send = database.get_users_by_time(current_time)
    
    for user in users_to_send:
        user_id = user["user_id"]
        mode = user["mode"]
        
        # Определяем, нужен ли звук (для мягкой доставки отключаем звук)
        is_silent = True if mode == "soft" else False
        
        welcome_text = (
            "Доброе утро! ✨\n\n"
            "Пришло время для Вашей утренней сонастройки. "
            "Выберите сферу жизни, которая сегодня требует Вашего наибольшего внимания:"
        )
        
        try:
            # 1. Переводим состояние пользователя в режим выбора сферы (извне хендлера)
            state_ctx = dp.fsm.resolve_context(bot, chat_id=user_id, user_id=user_id)
            await state_ctx.set_state(SoulSpaceStates.choosing_sphere)
            
            # 2. Отправляем сообщение (со звуком или без)
            await bot.send_message(
                chat_id=user_id,
                text=welcome_text,
                reply_markup=get_spheres_keyboard(),
                parse_mode="Markdown",
                disable_notification=is_silent
            )
        except Exception as e:
            print(f"Не удалось отправить утреннее сообщение пользователю {user_id}: {e}")

def start_scheduler():
    """Запуск планировщика, который срабатывает каждую минуту"""
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow") # Укажите ваш часовой пояс
    scheduler.add_job(check_morning_delivery, "cron", second=0) # Срабатывает ровно в 00 секунд каждой минуты
    scheduler.start()