from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import AUTH_BUTTON


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
    [AUTH_BUTTON]
        ], resize_keyboard=True)
    return markup


