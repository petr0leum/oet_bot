from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class CardButtons:
    CARD_BUTTON_LIKE = "👍 I like this card, keep it"
    CARD_BUTTON_REMAKE = "👎 I don't like this card, make me a new one"
    CARD_BUTTON_GAME = "🎮 Play a role play with this card"
    CARD_BUTTON_RETURN = "Return to menu"
    CARD_BUTTON_NO ="No, maybe later."

def rate_card_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=CardButtons.CARD_BUTTON_LIKE)
    builder.button(text=CardButtons.CARD_BUTTON_REMAKE)
    builder.button(text=CardButtons.CARD_BUTTON_RETURN)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def play_with_card_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=CardButtons.CARD_BUTTON_GAME)
    builder.button(text=CardButtons.CARD_BUTTON_NO)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)