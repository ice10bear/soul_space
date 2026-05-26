from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from openai import AsyncOpenAI
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
ai_client = AsyncOpenAI(base_url=config.BASE_URL, api_key=config.API_KEY)