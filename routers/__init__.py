__all__ = ("router",)

from aiogram import Router

from .handlers import router as handlers_router
from .commands import router as commands_router
from .common import router as common_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    handlers_router,
)

router.include_router(common_router) # this one has to be the last!?