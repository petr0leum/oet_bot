import asyncio
from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from config import settings
from llms_content import ai_patient_content
from routers.states import RolePlayState
from .generate_card import generate_scenario
from keyboards import ButtonText, get_on_start_kb, game_preparation_keyboard
from routers.handlers.game_handlers import update_timer_message
from utils import (
    format_json_to_markdown,
    take_patient_info_for_prompt
)

router = Router(name=__name__)


@router.message(F.text == ButtonText.PLAY_GAME)
@router.message(Command("play_game"))
async def play_game(message: types.Message, state: FSMContext, card_text: str = None):
    """
    Start a role play game with a generated scenario and handle the interaction.

    Args:
        message (types.Message): Incoming message triggering the role play game.
        state (FSMContext): Finite State Machine context for maintaining state data.
        card_data (str, optional): JSON string of the card data. Defaults to None.
    """
    try:
        caution_message = await message.reply(
            'When your card is ready you will have 3 minutes to prepare yourself.'
        )

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            if card_text:
                card_json = eval(card_text)
            else:
                card_json = await generate_scenario(message, state)

            _, _, doctor = format_json_to_markdown(card_json)
            patient_card = take_patient_info_for_prompt(card_json)

            messages = [{
                "role": "system", 
                "content": ai_patient_content.replace('__patient_card__', patient_card)
            }]

            await message.reply(
                doctor, 
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=game_preparation_keyboard()
            )

            await state.update_data(
                json_card=card_json,
                rp_messages=messages,
                dialog=[],
                last_bot_message_id=None,
            )
            
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=caution_message.message_id
        )

        await state.set_state(RolePlayState.Preparation)
        timer_message = await message.reply(
            text=markdown.text(
                markdown.markdown_decoration.quote(
                    f"Time remaining: 0{settings.time_to_read_card}:00"
                )
            ), 
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        await asyncio.create_task(
            update_timer_message(
                message.bot,
                message.chat.id,
                timer_message.message_id,
                datetime.now() + timedelta(minutes=settings.time_to_read_card)
            )
        )

        current_state = await state.get_state()
        if current_state == RolePlayState.Preparation.state:
            start_message = await message.reply(
                text = markdown.text(
                    markdown.markdown_decoration.quote(
                        "The preparation time is over. Please record your first voice message."
                    ),
                    "To stop the game __/cancel__",
                    sep='\n'
                ),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.set_state(RolePlayState.RolePlay)
            await state.update_data(
                start_message_id=start_message.message_id,
                rp_start_time=datetime.now(),
                rp_end_time=datetime.now() + timedelta(minutes=1), # settings.game_time
                rp_total_response_time=0
            )
        
    except TimeoutError:
        await message.reply(
            "Failed to generate a card. Please try again.",
            reply_markup=get_on_start_kb()
        )
