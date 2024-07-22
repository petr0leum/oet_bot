import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any

import torch
import torchaudio
import whisper
from gtts import gTTS
from openai import OpenAI
from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import settings
from keyboards.common_keyboards import ButtonText
from .generate_card import generate_scenario, chatbot_response

router = Router(name=__name__)


class RolePlayState(StatesGroup):
    role_play_active = State()
    start_time = State()
    stt_model = State()
    chat = State()
    total_response_time = State()

def load_audio(audio_path):
    """
    Load an audio file from the specified path and return the waveform and sample rate.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        waveform (Tensor): Tensor containing the audio waveform.
        sample_rate (int): Sample rate of the audio.
    """
    waveform, sample_rate = torchaudio.load(audio_path)
    return waveform, sample_rate

def create_audio_chunks(waveform, total_duration, sample_rate, chunk_duration=30):
    """
    Divide the audio waveform into chunks of specified duration.

    Args:
        waveform (Tensor): Tensor containing the audio waveform.
        total_duration (float): Total duration of the audio in seconds.
        sample_rate (int): Sample rate of the audio.
        chunk_duration (int, optional): Duration of each chunk in seconds. Default is 30 seconds.

    Returns:
        chunks (list): List of tensors, each containing a chunk of the audio.
        sample_rate (int): Sample rate of the audio.
    """
    chunks = []
    for start in range(0, int(total_duration), chunk_duration):
        end = min(start + chunk_duration, total_duration)
        chunk_waveform = waveform[:, int(start * sample_rate):int(end * sample_rate)]
        chunks.append(chunk_waveform)
    return chunks, sample_rate

def transcribe_with_whisper(model, device, audio_path):
    """
    Transcribe the audio file using the Whisper model.

    Args:
        model (Model): Whisper model instance.
        device (str): Device to use for processing ('cpu' or 'cuda').
        audio_path (str): Path to the audio file.

    Returns:
        str: Transcribed text from the audio.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"The file {audio_path} does not exist.")
    else:
        waveform, sample_rate = load_audio(audio_path)
        total_duration = waveform.size(1) / sample_rate

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. Please check your CUDA installation.")

    if total_duration <= 45:
        waveform = waveform.to(device)

        # Whisper expects audio to be resampled to 16000 Hz
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000).to(device)
        waveform = resampler(waveform)

        audio_tensor = waveform.squeeze(0).cpu().numpy()  # Whisper expects a 1D numpy array
        options = {"fp16": False, "language": None, "task": "transcribe"}
        result = model.transcribe(audio_tensor, **options)
        
        return result['text']
    else:
        chunks, sample_rate = create_audio_chunks(waveform, total_duration, sample_rate)
    
        # Whisper expects audio to be resampled to 16000 Hz
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000).to(device)
        transcriptions = []
    
        for chunk in chunks:
            chunk = chunk.to(device)
            chunk = resampler(chunk)
            
            with torch.cuda.amp.autocast():
                audio_tensor = chunk.squeeze(0).cpu().numpy()  # Whisper expects a 1D numpy array
                result = model.transcribe(audio_tensor)
                transcriptions.append(result['text'])
    
            torch.cuda.empty_cache()  # Release GPU memory
    
        return " ".join(transcriptions)
    
def create_audio(text, file_path='data/audio_storage/response.ogg'):
    """
    Convert text to speech and save it as an audio file.

    Args:
        text (str): Text to convert to speech.
        file_path (str, optional): Path to save the audio file. Default is 'data/audio_storage/response.ogg'.

    Returns:
        str: Path to the saved audio file.
    """
    tts = gTTS(text=text, lang='en')
    tts.save(file_path)  # Save the audio file
    return file_path

async def update_timer_message(context):
    """
    Update the timer message with the elapsed time.

    Args:
        context (ContextTypes.DEFAULT_TYPE): Context containing job information.
    """
    job = context.job
    elapsed_time = (datetime.now() - job.context['start_time']).total_seconds()
    minutes, seconds = divmod(elapsed_time, 60)
    time_str = f"{int(minutes):02}:{int(seconds):02}"
    try:
        await context.bot.edit_message_text(
            text=f"Итоговое время беседы: {time_str}",
            chat_id=job.context['chat_id'],
            message_id=job.context['timer_message_id']
        )
    except Exception as e:
        logging.error(f"Ошибка при обновлении таймера: {e}")

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

@router.message(F.text == ButtonText.PLAY_GAME or F.text == ButtonText.CARD_BUTTON_GAME)
@router.message(Command("play_game"))
async def play_game(message: types.Message, state: FSMContext):
    """
    Start a role play game with a generated scenario and handle the interaction.

    Args:
        message (types.Message): Incoming message triggering the role play game.
        state (FSMContext): Finite State Machine context for maintaining state data.
    """
    try:
        formatted_scenario, _ = await generate_scenario(message, state)

        await message.reply('You will now have 3 minutes to prepare, this is your card:')
        await message.reply(formatted_scenario, parse_mode=ParseMode.MARKDOWN)

        await asyncio.sleep(180)  # We wait for 3 minutes
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        whisper_model = whisper.load_model("base", device=device)
        client = OpenAI(
            api_key=settings.openai_api_token,
            organization=settings.openai_org_id,
            project=settings.openai_proj_oet
        )

        messages = [{
            "role": "system", 
            "content": formatted_scenario
        }]  # Append a system content

        await state.update_data(
            role_play_active=True,
            start_time=datetime.now(),
            stt_model={'device': device, 'model': whisper_model},
            chat={'client': client, 'messages': messages},
            total_response_time=0
        )

        timer_message = await message.reply("Итоговое время беседы: 00:00")
        await state.update_data(timer_message_id=timer_message.message_id)

        await message.reply("Role play started! Please record your first voice message.")

        while await state.get_data()['role_play_active']:
            await update_timer_message(message.bot, message.chat.id, timer_message.message_id, datetime.now())
            await asyncio.sleep(1)

    except TimeoutError:
        await message.reply("Failed to generate a card. Please try again.")

async def handle_voice(message: types.Message, state: FSMContext):
    """
    Handle voice messages during the role play game, including transcription and generating responses.

    Args:
        message (types.Message): Incoming voice message.
        state (FSMContext): Finite State Machine context for maintaining state data.
    """

    computing_start_ = datetime.now()
    state_data = await state.get_data()
    timer_status = await time_check(
        datetime.now(), 
        state_data['start_time'], 
        state_data['total_response_time']
    )

    if state_data.get('role_play_active', False) and timer_status:
        logging.info("Processing voice message")
        voice = message.voice
        file = await voice.get_file()
        file_path = os.path.join('data', 'temp_audio_files', 'voice.mp3')
        await file.download(file_path)
        logging.info("File downloaded")

        # Transcribe audio file
        logging.info("Starting transcription")
        transcription = transcribe_with_whisper(
            state_data['stt_model']['model'],
            state_data['stt_model']['device'],
            file_path
        )
        state_data['chat']['messages'].append(
            {"role": "user", "content": transcription}
        )  # Append user's message
        logging.info(f"Transcription result: {transcription}")

        # Get GPT response
        logging.info("Getting GPT response")
        gpt_response = chatbot_response(
            state_data['chat']['client'], state_data['chat']['messages'], max_tokens=1000
        )
        state_data['chat']['messages'].append(
            {"role": "assistant", "content": gpt_response}
        )  # Append assistant's message
        logging.info(f"GPT response: {gpt_response}")

        # Convert GPT response to speech
        logging.info("Converting GPT response to audio")
        response_file_path = create_audio(gpt_response)
        logging.info(f"Audio file saved as {response_file_path}")

        # Send the response back as a voice message
        logging.info("Sending audio response")
        await message.reply_voice(voice=open(response_file_path, 'rb'))
        state_data['total_response_time'] += (datetime.now() - computing_start_).total_seconds()

        # Check if role play time is over
        timer_status = await time_check(
            datetime.now(), 
            state_data['start_time'], 
            state_data['total_response_time']
        )
    else:
        await message.reply_text("Игра окончена. Идет оценка диалога...")
        await asyncio.sleep(3)  # Pause for evaluation
        await message.reply_text("Шучу, это все, пока")

    logging.info("Waiting for next message")
