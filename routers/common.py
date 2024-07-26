from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import get_on_start_kb

router = Router(name=__name__)


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.reply(
            text="OK, but nothing was going on.",
            reply_markup=get_on_start_kb(),
        )
        return

    await state.clear()
    await message.answer(
        f"Cancelled state {current_state}.",
        reply_markup=get_on_start_kb(),
    )

@router.message()
async def handler(message: types.Message, state: FSMContext) -> None:
    """
    Handle any message
    """
    await state.clear()
    await message.answer(
        f"Bad request. Use Buttons",
        reply_markup=get_on_start_kb(),
    )
