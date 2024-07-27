import random
from typing import List, Dict, Any
from openai import OpenAI

from config import settings
from llms_content import (
    oet_cards,
    few_shot_content, 
    oet_card_question,
    ideal_card_question,
    bad_card_question,
    good_card_question
)



client = OpenAI(
    api_key=settings.openai_api_token,
    organization=settings.openai_org_id,
    project=settings.openai_proj_oet
)

def generate_prompt(good_gen_cards: List[Dict[str, Any]],
                    bad_gen_cards: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Generate a prompt using different cards examples from the provided examples. 
    This includes a mix of ideal cards, good cards, and bad cards examples.

    Args:
        prompt_examples (List[Dict[str, Any]]): List of few-shot example dictionaries.

    Returns:
        List[Dict[str, str]]: A list of messages to be used as a prompt for the chatbot.
    """
    content_real_card = random.sample(oet_cards, 1)
    remaining_examples = random.sample(
        [example for example in oet_cards if example not in content_real_card], 
        settings.card_examples_num
    )

    messages = [
        {
            "role": "system", 
            "content": few_shot_content.replace('__ideal_card__', str(content_real_card))
        }
    ]
    messages.append({"role": "user", "content": oet_card_question})

    for ex in remaining_examples:
        messages.append({"role": "assistant", "content": f"{ex}"})
        messages.append({"role": "user", "content": ideal_card_question})
    
    if bad_gen_cards:
        for ex in bad_gen_cards:
            messages.append({"role": "assistant", "content": f"{ex}"})
            messages.append({"role": "user", "content": bad_card_question})
        
    if good_gen_cards:
        for ex in good_gen_cards:
            messages.append({"role": "assistant", "content": f"{ex}"})
            messages.append({"role": "user", "content": good_card_question})
    
    return messages

def chatbot_response(messages: List[Dict[str, str]], 
                     max_tokens: int = 1000, 
                     response_format: str = "text") -> str:
    """
    Generate a response from the chatbot based on the provided messages.

    Args:
        client (OpenAI): OpenAI client instance.
        messages (List[Dict[str, str]]): List of messages to send to the chatbot.
        max_tokens (int, optional): Maximum number of tokens in the response. Defaults to 1000.

    Returns:
        str: The generated response from the chatbot.
    """
    '''Generate chatbot response'''

    completion = client.chat.completions.create(
        model=settings.chat_model,
        response_format={"type": response_format},
        messages=messages,
        max_tokens=max_tokens
    )
    
    output_text = completion.choices[0].message.content
    return output_text

def check_generated_card(card: str) -> dict:
    """
    Validate the structure and content of a generated card in JSON format.

    Args:
        card (str): A JSON string representing the generated card.

    Raises:
        AssertionError: If the expected keys are not present in the JSON or if the number of tasks is incorrect.

    Returns:
        dict: The parsed JSON content of the card if all checks pass.
    """
    card_json = eval(card)

    expected_keys = {'SETTINGS', 'PATIENT_CARD', 'DOCTOR_CARD', 'PATIENT_TASK', 'DOCTOR_TASK'}
    actual_keys = set(card_json.keys())
    assert expected_keys.issubset(actual_keys), (
        f"Error in JSON keys. Expected keys: {expected_keys}. Received keys: {actual_keys}"
    )

    patient_tasks_len = len(card_json['PATIENT_TASK'])
    doctor_tasks_len = len(card_json['DOCTOR_TASK'])
    assert patient_tasks_len == 5, f"Error: the number of patient tasks should be 5. Received: {patient_tasks_len}"
    assert doctor_tasks_len == 5, f"Error: the number of doctor tasks should be 5. Received: {doctor_tasks_len}"

    return card_json
