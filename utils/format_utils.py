from io import StringIO
from typing import Dict, Any
from aiogram.utils import markdown


def convert_json_to_text(card_data: Dict[str, Any]) -> StringIO:
    """
    Convert JSON data to text.

    Args:
        card_data (Dict[str, Any]): Dictionary containing card data with keys
        'SETTINGS', 'PATIENT_CARD', 'PATIENT_TASK', 'DOCTOR_CARD' and 'DOCTOR_TASK'.

    Returns:
        StringIO: A buffer containing the formatted card text.
    """
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
    """
    Format JSON data to markdown.

    Args:
        json_data (Dict[str, Any]): Dictionary containing card data with keys 
        'SETTINGS', 'PATIENT_CARD', 'PATIENT_TASK', 'DOCTOR_CARD' and 'DOCTOR_TASK'.

    Returns:
        Tuple[str, str, str]: A tuple containing the formatted markdown string of the entire card,
        the patient card part, and the doctor card part.
    """
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

def take_patient_info_for_prompt(json_data: Dict[str, Any]) -> str:
    patient_tasks = "\n".join([f"* {task}" for task in json_data['PATIENT_TASK']])
    patient_card = f'''
    'A place where the event takes place': {json_data['SETTINGS']},
    'A description of your situation and the reason for the visit': {json_data['PATIENT_CARD']},
    'Tasks you need to complete during your long dialogue with your doctor': {patient_tasks},
    '''
    return patient_card
