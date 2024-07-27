import logging

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.utils.chat_action import ChatActionSender

from database import get_last_user_cards
from keyboards import (
    ButtonText,
    get_on_start_kb,
    rate_card_keyboard
)
from utils import (
    check_generated_card,
    chatbot_response,
    generate_prompt,
    format_json_to_markdown,
    convert_json_to_text
)

router = Router(name=__name__)


async def generate_scenario(message: types.Message, state: FSMContext):
    """
    Generate an OET scenario.

    Returns: dict: The parsed JSON content of the generated card if all checks pass.

    Raises:
        AssertionError: If the generated card's structure is incorrect.
        Exception: For any other errors during the generation process.
    """
    try:
        state_data = await state.get_data()

        user_id = str(message.from_user.id)
        bad_examples = state_data.get('recent_disliked_cards', None)
        good_examples = get_last_user_cards(user_id) # Get cards that user liked before

        prompt = generate_prompt(good_examples, bad_examples)
        gen_card = chatbot_response(prompt, response_format="json_object")
        
        card_json = check_generated_card(gen_card)
        await state.update_data(current_card=gen_card)

        return card_json
    
    except AssertionError as e:
        logging.error(f"Error in card structure: {e}")
        await state.clear()
        await message.reply(
            "Failed to generate a card. Please try again.", 
            reply_markup=get_on_start_kb()
        )

    except Exception as e:
        logging.error(f"Error with card generation!")
        await state.clear()
        await message.reply(
            "Failed to generate a card. Please try again.", 
            reply_markup=get_on_start_kb()
        )

@router.message(F.text == ButtonText.GENERATE_CARD, default_state)
@router.message(Command("generate_card"), default_state)
async def generate_card(message: types.Message, state: FSMContext) -> None:
    """
    Handle the /generate_card command.
    """
    caution_message = await message.reply(
        markdown.text(
            markdown.markdown_decoration.quote("⏱️ Generating a card..."),
            markdown.text(
                markdown.markdown_decoration.quote("Please wait, "),
                markdown.bold('it will take some time.'),
            ),
            sep="\n"
        ), 
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    async with ChatActionSender.typing(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        card_json = await generate_scenario(message, state)
    
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=caution_message.message_id
    )

    document_message = await message.reply_document(
        document=types.BufferedInputFile(
            file=convert_json_to_text(card_json).getvalue().encode("utf-8"),
            filename="card.txt"
        )
    )
    await state.update_data(current_doc_message_id=document_message.message_id)
    
    text_message = await message.bot.send_message(
        chat_id=message.chat.id,
        text=format_json_to_markdown(card_json)[0],
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=rate_card_keyboard(),
        reply_to_message_id=document_message.message_id
    )
    await state.update_data(current_text_message_id=text_message.message_id)
