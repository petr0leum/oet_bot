import os
import logging
import asyncio
from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from config import settings
from llms_content import dialog_score_prompt, only_score_prompt
from routers.states import RolePlayState
from keyboards import GameButtons, get_on_start_kb, game_results_keyboard
from utils.openai_utils import chatbot_response
from utils.audio_utils import transcribe_with_whisper, create_audio

router = Router(name=__name__)


async def time_check(current_time, start_time, comput_time):
    """
    Check if the role play game time is still within the allowed duration.

    Args:
        current_time (datetime): Current time.
        start_time (datetime): Start time of the game.
        comput_time (float): Accumulated computation time in seconds.

    Returns:
        bool: True if the game time is within the allowed duration, False otherwise.
    """
    elapsed_time = (current_time - start_time).total_seconds()
    return elapsed_time - comput_time <= settings.game_time * 60

async def update_timer_message(bot, chat_id, message_id, end_time):
    """
    Update the timer message with the remaining time.

    Args:
        bot (Bot): Bot instance.
        chat_id (int): Chat ID.
        message_id (int): Timer message ID.
        end_time (datetime): End time of the timer.
    """
    while True:
        now = datetime.now()
        remaining_time = end_time - now
        if remaining_time <= timedelta(0):
            break

        minutes, seconds = divmod(remaining_time.total_seconds(), 60)
        time_str = f"{int(minutes):02}:{int(seconds):02}"

        try:
            text = markdown.text(
                markdown.bold(f"Time remaining:"),
                markdown.text(f"{time_str}")
            )
            await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except Exception as e:
            logging.error(f"Error updating timer: {e}")
            if "message can't be edited" in str(e):
                logging.error(f"Cannot edit message {message_id} in chat {chat_id}")
                break

        await asyncio.sleep(1)

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

@router.message(RolePlayState.RolePlay, F.voice)
async def handle_voice(message: types.Message, state: FSMContext):
    """
    Handle voice messages during the role play game, including transcription and generating responses.
    """
    computing_start_ = datetime.now()
    state_data = await state.get_data()
    timer_status = await time_check(datetime.now(), state_data['rp_start_time'], 
                                    state_data['rp_total_response_time'])
    
    file_info = await message.bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    local_file_path = os.path.join('data', 'audio_storage', 'voice.ogg')
    await message.bot.download_file(file_path, local_file_path)

    # Transcribe audio file
    transcription = transcribe_with_whisper(local_file_path)
    state_data['rp_messages'].append({"role": "user", "content": transcription})
    
    if timer_status:
        async with ChatActionSender.record_voice(
            bot=message.bot,
            chat_id=message.chat.id,
        ):
            
            if state_data.get('last_bot_message_id'):
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=state_data['last_bot_message_id']
            )

            # Get GPT response
            gpt_response = chatbot_response(state_data['rp_messages'], max_tokens=200)
            state_data['rp_messages'].append({"role": "assistant", "content": gpt_response})

            # Convert GPT response to speech
            response_file_path = create_audio(gpt_response)

            # Send the response back as a voice message
            voice_file = FSInputFile(response_file_path)
            bot_message = await message.answer_voice(voice=voice_file)

        await state.update_data(last_bot_message_id=bot_message.message_id)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        state_data['rp_total_response_time'] += (datetime.now() - computing_start_).total_seconds()

        dialog = state_data.get('dialog', []) # Save dialog
        dialog.append({"user": transcription, "assistant": gpt_response})

        await state.update_data(dialog=dialog)
    else:
        await state.update_data(dialog=state_data.get('dialog', []) + [{"user": transcription, "assistant": ""}])
        if state_data.get('last_bot_message_id'):
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=state_data['last_bot_message_id']
        )
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.set_state(RolePlayState.ResultsEvaluation)
        await message.answer(
            "The game is over. What do you want to do next?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=game_results_keyboard()
            )

    logging.info("Waiting for next message")

@router.message(RolePlayState.RolePlay, Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    await state.clear()
    await message.answer(
        f"Too bad you stopped the game, try again!",
        reply_markup=get_on_start_kb(),
    )

@router.message(RolePlayState.RolePlay)
async def handle_role_play_invalid_message(message: types.Message):
    await message.answer(
        text="Invalid message type, please send me only voice messages while we are playing. Cancel role play? Tap __/cancel__",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(RolePlayState.Preparation, F.text == GameButtons.GAME_STOP_PREP)
async def end_preparation_early(message: types.Message, state: FSMContext):
    """
    End the preparation period early and start the role play game.
    """
    await message.delete()

    logging.info('--------------------Статус ИГРЫ досрочно')
    await state.set_state(RolePlayState.RolePlay)
    await state.update_data(
        rp_start_time=datetime.now(),
        rp_end_time=datetime.now() + timedelta(minutes=0.6), # settings.game_time
        rp_total_response_time=0
    )

    await message.answer(
        text = markdown.text(
            markdown.markdown_decoration.quote(
                "Role play started! Please record your first voice message."
            ),
            "To stop the game __/cancel__",
            sep='\n'
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(RolePlayState.ResultsEvaluation, F.text == GameButtons.GAME_SEND_TEXT)
async def get_dialog_text(message: types.Message, state: FSMContext):
    """
    Send the dialog text to the user.
    """
    state_data = await state.get_data()

    if state_data.get('text_sent', False):
        await message.reply("The dialogue has already been sent to you.")
        return
    
    async with ChatActionSender.upload_document(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        card = state_data.get('json_card', '')
        dialog = state_data.get('dialog', [])
        if not dialog:
            await message.reply("No dialog found.")
            return

        dialog_text = f"{card}\n\n"
        for turn in dialog:
            dialog_text += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

        await message.reply_document(
            document=types.BufferedInputFile(
                file=dialog_text.encode("utf-8"),
                filename="dialog.txt"
            )
        )

    await message.answer("Anything else?", reply_markup=game_results_keyboard())
    await state.update_data(text_sent=True)

@router.message(RolePlayState.ResultsEvaluation, F.text == GameButtons.GAME_EVALUATE_DIALOGUE)
async def score_dialog(message: types.Message, state: FSMContext):
    """
    Ask ChatGPT to score the dialog based on known criteria.
    """
    state_data = await state.get_data()

    if state_data.get('dialog_evaluated', False):
        await message.reply("The dialogue has already been evaluated.")
        return
    
    dialog = state_data.get('dialog', [])
    if not dialog:
        await message.reply("No dialog found.")
        return

    async with ChatActionSender.upload_document(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        dialog_text = ""
        for turn in dialog:
            dialog_text += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

        prompt = dialog_score_prompt.replace('__dialogue__', dialog_text)
        messages = [{"role": "system", "content": prompt}]

        gpt_response = chatbot_response(messages, max_tokens=1000)

        score_responce = f"Dialogue score and feedback:\n\n{gpt_response}"
        await message.reply_document(
            document=types.BufferedInputFile(
                file=score_responce.encode("utf-8"),
                filename="score.txt"
            )
        )

    messages.append({"role": "assistant", "content": gpt_response})
    messages.append({"role": "user", "content": only_score_prompt})

    score = chatbot_response(messages, max_tokens=10)

    text = markdown.text(
        markdown.text(
            "Your score is ",
            score,
            markdown.markdown_decoration.quote("."),
            sep=''
        ),
        markdown.markdown_decoration.quote("Anything else?"),
        sep='\n'
    )
    await message.answer(
        text=text, 
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=game_results_keyboard()
    )

    await state.update_data(dialog_evaluated=True)

@router.message(RolePlayState.ResultsEvaluation, F.text == GameButtons.GAME_CLOSE)
async def return_to_menu(message: types.Message, state: FSMContext) -> None:
    """
    Return to menu and clear all states.
    """
    await state.clear()
    await message.reply("Returning to the main menu.", reply_markup=get_on_start_kb())