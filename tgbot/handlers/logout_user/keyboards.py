from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.logout_user.static_text import START_BUTTON


def start_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [START_BUTTON]
    ], resize_keyboard=True)
    return markup
