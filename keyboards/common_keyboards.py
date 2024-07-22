from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ButtonText:
    ##  MAIN COMMANDS
    GENERATE_CARD = "Generate a card"
    PLAY_GAME = "Start a role play with AI"
    SHOW_CARDS = "Show previosly generated cards"
    HELP = "Need help"
    STOP = "Stop the bot"
    ## EXTRA
    CARD_BUTTON_LIKE = "👍 I like this card, keep it"
    CARD_BUTTON_REMAKE = "👎 I don't like this card, make me a new one"
    CARD_BUTTON_GAME = "🎮 Play a role play with this card"

def get_on_start_kb() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ButtonText.GENERATE_CARD)], 
            [KeyboardButton(text=ButtonText.PLAY_GAME)], 
            [KeyboardButton(text=ButtonText.SHOW_CARDS)],
            [KeyboardButton(text=ButtonText.HELP), KeyboardButton(text=ButtonText.STOP)]
        ],
        resize_keyboard=True,
        # one_time_keyboard=True,
    )
    return markup

def get_on_help_kb() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ButtonText.GENERATE_CARD)], 
            [KeyboardButton(text=ButtonText.PLAY_GAME)], 
            [KeyboardButton(text=ButtonText.SHOW_CARDS)],
        ],
        resize_keyboard=True,
    )
    return markup

def build_card_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=ButtonText.CARD_BUTTON_LIKE)
    builder.button(text=ButtonText.CARD_BUTTON_REMAKE)
    builder.button(text=ButtonText.CARD_BUTTON_GAME)
    return builder.as_markup(resize_keyboard=True)