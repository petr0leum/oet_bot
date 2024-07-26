from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class GameButtons:
    GAME_STOP_PREP = "Enough preparations, I'm ready."
    GAME_EVALUATE_DIALOGUE = "💯 Score the dialogue"
    GAME_SEND_TEXT = "Send dialogue record and the role play card"
    GAME_CLOSE = "Return to menu"

def game_preparation_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=GameButtons.GAME_STOP_PREP)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def game_results_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=GameButtons.GAME_SEND_TEXT)
    builder.button(text=GameButtons.GAME_EVALUATE_DIALOGUE)
    builder.button(text=GameButtons.GAME_CLOSE)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)