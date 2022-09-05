from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import aiogram.utils.markdown as fmt


def get_buttons_of_categories(categories):
    inline_kb = InlineKeyboardMarkup()
    for category in categories:
        button = InlineKeyboardButton(category.get('name'), callback_data=category.get('link'))
        inline_kb.add(button)

    return inline_kb


def generate_button(data: dict) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for label, callback_data in data.items():
        button = InlineKeyboardButton(text=label, callback_data=callback_data, )
        inline_kb.add(button)

    return inline_kb
