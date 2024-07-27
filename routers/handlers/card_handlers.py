import logging
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from config import settings
from database import save_user_card
from routers.states import CardState
from routers.commands.role_play_game import play_game
from routers.commands.generate_card import generate_card
from keyboards import (
    CardButtons, 
    get_on_start_kb,
    play_with_card_keyboard
)

router = Router(name=__name__)


@router.message(F.text == CardButtons.CARD_BUTTON_REMAKE)
async def regenerate_card(message: types.Message, state: FSMContext) -> None:
    """
    Handle the "remake card" button, delete previous messages, and regenerate a card.
    """
    try:
        state_data = await state.get_data()
        document_message_id = state_data.get("current_doc_message_id")
        text_message_id = state_data.get("current_text_message_id")
        current_card = state_data.get('current_card')

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=document_message_id
        )
        
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=text_message_id
        )
    except Exception as e:
        logging.error(f"Error deleting previous message: {e}")
    
    recent_disliked_cards = state_data.get('recent_disliked_cards', [])
    recent_disliked_cards.append(current_card)

    if len(recent_disliked_cards) > settings.card_examples_num:
        recent_disliked_cards.pop(0)  # Keep only the last 5 disliked cards

    await state.update_data(recent_disliked_cards=recent_disliked_cards)
    await generate_card(message, state)

@router.message(F.text == CardButtons.CARD_BUTTON_LIKE)
async def keep_card_and_play_game(message: types.Message, state: FSMContext) -> None:
    """
    Handle the "like card" button, save the card, and suggest role play.
    """
    user_id = message.from_user.id

    data = await state.get_data()
    card_data = data.get('current_card', '')

    if card_data:
        save_user_card(user_id, card_data)

    await state.set_state(CardState.GoodCard)
    await message.reply(
        markdown.text(
            markdown.text(
                "The card has been ",
                markdown.bold('saved'),
                markdown.markdown_decoration.quote(".")
            ),
            '',
            markdown.text(
                "It",
                markdown.bold("will be used"),
                "to generate",
                markdown.bold("the next cards"),
                markdown.markdown_decoration.quote("for you.")
            ),
            markdown.code(
                "The last 5 saved cards are used to generate new cards, so try to save only good ones!"
            ),
            '',
            markdown.text(
                markdown.markdown_decoration.quote("Do you want to start a"),
                markdown.bold('🎮 role play'),
                markdown.markdown_decoration.quote("with this card?")
            ),
            sep="\n"
        ), 
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=play_with_card_keyboard()
    )

@router.message(CardState.GoodCard, F.text == CardButtons.CARD_BUTTON_GAME)
async def start_role_play(message: types.Message, state: FSMContext) -> None:
    """
    Start role play game with the kept card.
    """
    data = await state.get_data()
    card_data = data.get('current_card', '')

    if card_data:
        await state.clear()
        await play_game(message, state, card_data)
    else:
        await state.clear()
        await message.reply(
            "No card found. Please generate a card first.", 
            reply_markup=get_on_start_kb()
        )

@router.message(F.text.in_([CardButtons.CARD_BUTTON_NO, CardButtons.CARD_BUTTON_RETURN]))
async def return_to_main_menu(message: types.Message, state: FSMContext) -> None:
    """
    Return to the main menu and clear all states.
    """
    await state.clear()
    await message.reply("Returning to the main menu.", reply_markup=get_on_start_kb())
