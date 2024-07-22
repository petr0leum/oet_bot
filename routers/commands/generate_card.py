import random
import logging
from io import StringIO
from typing import List, Dict, Any

from openai import OpenAI
from aiogram import Router, types, F
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.common_keyboards import (
    ButtonText,
    get_on_start_kb,
    build_card_keyboard
)
from database import save_user_card
from config import settings
from llms_content import few_shot_content, oet_cards

router = Router(name=__name__)


class CardState(StatesGroup):
    current_card = State()
    current_doc_message_id = State()
    current_text_message_id = State()

def search_for_disease(examples: List[Dict[str, Any]], disease: str) -> List[Dict[str, Any]]:
    '''Search for examples with exact disease'''
    return [card for card in examples if disease.lower() in card['question'].lower()]

def fetch_few_shot_examples(examples: List[Dict[str, Any]], 
                            disease: str = 'not stated', 
                            num_examples: int = 3) -> List[Dict[str, Any]]:
    if disease != 'not stated':
        examples = search_for_disease(examples, disease)
    prompt_examples = random.sample(examples, num_examples)
    return prompt_examples

def generate_prompt(prompt_examples: List[Dict[str, Any]], disease: str = 'not stated') -> List[Dict[str, str]]:
    messages = [
        {"role": "system", "content": few_shot_content}
    ]
    
    for ex in prompt_examples:
        messages.append({"role": "user", "content": ex['question']})
        messages.append({"role": "assistant", "content": ex['answer']})
    
    messages.append({"role": "user", "content": f"Generate a card for speaking role play in OET exam. The card must be in JSON format with 5 keys: SETTINGS; PATIENT_CARD; PATIENT_TASK; DOCTOR_CARD; DOCTOR_TASK. The disease is {disease}"})
    
    return messages

def chatbot_response(client: OpenAI, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
    '''Generate chatbot response'''
    completion = client.chat.completions.create(
        model=settings.chat_model,
        response_format={"type": "json_object"},
        messages=messages,
        max_tokens=max_tokens
    )
    
    output_text = completion.choices[0].message.content
    return output_text

def generate_oet_card_text(card_data: Dict[str, Any]) -> StringIO:
    '''Generate OET card text from JSON data'''
    buffer = StringIO()
    
    buffer.write("# OET Exam Role Play Card\n\n")
    buffer.write(f"## Setting: {card_data['SETTINGS']}\n\n")
    buffer.write(f"## Patient Card\n{card_data['PATIENT_CARD']}\n\n")
    buffer.write("## Patient Tasks\n")
    for i, task in enumerate(card_data['PATIENT_TASK'], 1):
        buffer.write(f"{i}. {task}\n")
        
    buffer.write(f"\n## Doctor Card\n{card_data['DOCTOR_CARD']}\n\n")
    buffer.write("## Doctor Tasks\n")
    for i, task in enumerate(card_data['DOCTOR_TASK'], 1):
        buffer.write(f"{i}. {task}\n")
    
    buffer.seek(0)
    return buffer

def format_json_to_markdown(json_data: Dict[str, Any]) -> str:
    '''Format JSON data to markdown'''
    patient_tasks = "\n".join([f"* {task}" for task in json_data['PATIENT_TASK']])
    doctor_tasks = "\n".join([f"* {task}" for task in json_data['DOCTOR_TASK']])

    formatted_text_patient = markdown.text(
        markdown.bold(
            markdown.markdown_decoration.quote("Setting:")
        ),
        markdown.markdown_decoration.quote(f"{json_data['SETTINGS']}"),
        markdown.bold(
            markdown.markdown_decoration.quote("Patient:")
        ),
        markdown.markdown_decoration.quote(f"{json_data['PATIENT_CARD']}"),
        markdown.bold(
            markdown.markdown_decoration.quote("Patient Tasks:")
        ),
        markdown.markdown_decoration.quote(patient_tasks),
        sep="\n"
    )
    formatted_text_doctor = markdown.text(
        markdown.bold(
            markdown.markdown_decoration.quote("Setting:")
        ),
        markdown.markdown_decoration.quote(f"{json_data['SETTINGS']}"),
        markdown.bold(
            markdown.markdown_decoration.quote("Doctor:")
        ),
        markdown.markdown_decoration.quote(f"{json_data['DOCTOR_CARD']}"),
        markdown.bold(
            markdown.markdown_decoration.quote("Doctor Tasks:")
        ),
        markdown.markdown_decoration.quote(doctor_tasks),
        sep="\n"
    )

    formatted_text = markdown.text(
        markdown.markdown_decoration.bold(
            markdown.underline(
                 markdown.markdown_decoration.quote("Patient Card:") 
            )
        ),
        markdown.markdown_decoration.spoiler(formatted_text_patient),
        markdown.markdown_decoration.bold(
            markdown.underline(
                 markdown.markdown_decoration.quote("Doctor Card:") 
            )
        ),
        formatted_text_doctor,
        sep="\n"
    )
    return formatted_text, formatted_text_patient, formatted_text_doctor

async def generate_scenario(message: types.Message, state: FSMContext):
    '''Generate OET scenario'''
    oet_client = OpenAI(api_key=settings.openai_api_token,
                    organization=settings.openai_org_id,
                    project=settings.openai_proj_oet)
    try:
        logging.info('--------------- Генерируем примеры')
        few_shot_examples = fetch_few_shot_examples(oet_cards)
        logging.info('--------------- Генерируем промпт')
        prompt = generate_prompt(few_shot_examples)
        logging.info('--------------- Генерируем карточку')
        gen_card = chatbot_response(oet_client, prompt)
        logging.info(gen_card)

        logging.info('--------------- Проверяем карточку')
        card_json = eval(gen_card)

        # Проверка наличия всех необходимых ключей
        expected_keys = {'SETTINGS', 'PATIENT_CARD', 'DOCTOR_CARD', 'PATIENT_TASK', 'DOCTOR_TASK'}
        actual_keys = set(card_json.keys())
        assert expected_keys.issubset(actual_keys), f"Ошибка в ключах JSON. Ожидаемые ключи: {expected_keys}. Полученные ключи: {actual_keys}"

        patient_tasks_len = len(card_json['PATIENT_TASK'])
        doctor_tasks_len = len(card_json['DOCTOR_TASK'])
        assert patient_tasks_len == 5, f"Ошибка: количество задач пациента должно быть 5. Получено: {patient_tasks_len}"
        assert doctor_tasks_len == 5, f"Ошибка: количество задач доктора должно быть 5. Получено: {doctor_tasks_len}"
        logging.info('--------------- !!!!Карта прошла проверку')

        logging.info('--------------- Кладем карточку в буфер')
        file = generate_oet_card_text(card_json)

        logging.info('--------------- Форматируем карточку для отправки текста')
        formated_card, _, _ = format_json_to_markdown(card_json)

        await state.update_data(current_card=gen_card)

        logging.info('--------------- Отсылаем документ')
        document_message = await message.reply_document(
            document=types.BufferedInputFile(
                file=file.getvalue().encode("utf-8"),
                filename="card.txt"
            )
        )
        await state.update_data(current_doc_message_id=document_message.message_id)
        
        logging.info('--------------- Отсылаем текст')
        text_message = await message.bot.send_message(
            chat_id=message.chat.id,
            text=formated_card,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=build_card_keyboard(),
            reply_to_message_id=document_message.message_id
        )
        await state.update_data(current_text_message_id=text_message.message_id)
    
    except AssertionError as e:
        logging.error(f"Ошибка в структуре карточки: {e}")
        await message.reply("Failed to generate a card. Please try again.")

    except Exception as e:
        logging.error(f"Ошибка с карточкой!")
        await message.reply("Failed to generate a card. Please try again.")

@router.message(F.text == ButtonText.GENERATE_CARD)
@router.message(Command("generate_card"))
async def generate_card(message: types.Message, state: FSMContext) -> None:
    '''Handle the /generate_card command'''
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    async with ChatActionSender.typing(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        await generate_scenario(message, state)

@router.message(F.text == ButtonText.CARD_BUTTON_LIKE)
async def keep_card(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    data = await state.get_data()
    card_data = data.get('current_card', '')

    if card_data:
        save_user_card(user_id, card_data)

    await message.reply(
        "Great! The card has been kept. Returning to the main menu.",
        reply_markup=get_on_start_kb()
    )

@router.message(F.text == ButtonText.CARD_BUTTON_REMAKE)
async def regenerate_card(message: types.Message, state: FSMContext) -> None:
    try:
        state_data = await state.get_data()
        document_message_id = state_data.get("current_doc_message_id")
        text_message_id = state_data.get("current_text_message_id")

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=document_message_id
        )
        
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=text_message_id
        )
    except Exception as e:
        logging.error(f"Ошибка при удалении предыдущего сообщения: {e}")
    
    await generate_card(message, state)
