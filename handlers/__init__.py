from aiogram import Router
from .start import router as start_router
from .sphere import router as sphere_router
from .settings import router as settings_router # Импортируем настройки

router = Router()

# Объединяем три роутера под одной крышей
router.include_routers(start_router, sphere_router, settings_router)