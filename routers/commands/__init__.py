__all__ = ("router",)

from aiogram import Router

from .base_commands import router as base_commands_router
from .generate_card import router as generate_card_router
from .role_play_game import router as role_play_router
from .view_liked_cards import router as view_cards_router

router = Router(name=__name__)

router.include_routers(
    base_commands_router,
    generate_card_router,
    role_play_router,
    view_cards_router
)