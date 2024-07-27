from aiogram import Router

from .cards_view_callback_handlers import router as cards_view_callback_router

router = Router(name=__name__)

router.include_routers(
    cards_view_callback_router
)