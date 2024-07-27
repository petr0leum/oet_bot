from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database import get_card_by_id, get_last_user_card_ids
from utils import format_json_to_markdown

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("view_card_"))
async def view_card(callback_query: types.CallbackQuery):
    try:
        card_id = callback_query.data.split("_")[2]
        user_id = str(callback_query.from_user.id)
        real_card_ids = get_last_user_card_ids(user_id)
        card = get_card_by_id(user_id, real_card_ids[int(card_id)])
        
        if not card:
            await callback_query.message.reply("Card not found.")
            return

        card_text = format_json_to_markdown(eval(card.card_data))[0]
        await callback_query.message.reply(card_text, parse_mode=ParseMode.MARKDOWN_V2)
    except:
        await callback_query.message.reply('Card not found.')