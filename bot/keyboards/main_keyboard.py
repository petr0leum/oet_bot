from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton('/help'))
main_keyboard.add(KeyboardButton('/generate_role_play_card'))
main_keyboard.add(KeyboardButton('/play_role_game'))
main_keyboard.add(KeyboardButton('/materials'))
