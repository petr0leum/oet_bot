from aiogram import Router

from .card_handlers import router as card_handlers_router
from .game_handlers import router as game_handlers_router

router = Router(name=__name__)

router.include_routers(
    card_handlers_router,
    game_handlers_router,
)