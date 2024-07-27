from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class ButtonText:
    HELP = "⁉️ Need help"
    GENERATE_CARD = "🪪 Generate a card"
    PLAY_GAME = "🤖 Start a role play with AI"
    SHOW_CARDS = "💾 Show previosly generated cards"

def get_on_start_kb() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ButtonText.HELP)],
            [KeyboardButton(text=ButtonText.GENERATE_CARD)], 
            [KeyboardButton(text=ButtonText.PLAY_GAME)], 
            [KeyboardButton(text=ButtonText.SHOW_CARDS)],
        ],
        resize_keyboard=True
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
