import asyncio
import logging
from aiogram.types import BotCommand
from loader import bot, dp
from handlers import router as main_router
import database
from scheduler import start_scheduler # Импортируем планировщик

async def set_main_menu(bot):
    main_menu_commands = [
        BotCommand(command="/start", description="✨ Начать сонастройку"),
        BotCommand(command="/settings", description="⚙️ Настройка времени доставки")
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    logging.basicConfig(level=logging.INFO)
    
    database.init_db()
    await set_main_menu(bot)
    
    # ЗАПУСКАЕМ НАШ БУДИЛЬНИК ⏰
    start_scheduler()
    
    dp.include_router(main_router)
    
    print("✨ SoulSpace запущен! Автодоставка сообщений активна. ✨")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())