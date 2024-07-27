from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import get_last_user_card_ids
from keyboards import ButtonText
from config import settings


router = Router()

@router.message(F.text == ButtonText.SHOW_CARDS)
@router.message(Command("show_liked_cards"))
async def show_liked_cards(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    liked_cards = get_last_user_card_ids(user_id)

    if len(liked_cards) == 0:
        await message.reply("You have no liked cards.")
        return

    card_buttons = [
            types.InlineKeyboardButton(
                text=f"Card {i+1}",
                callback_data=f"view_card_{i}"
            ) for i in range(len(liked_cards))
        ]
    
    inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[card_buttons])
    
    await message.reply(
        f"Here are your last {settings.card_examples_num} liked cards. Select one to view:", 
        reply_markup=inline_kb
    )