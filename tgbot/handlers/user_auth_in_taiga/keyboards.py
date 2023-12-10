from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.user_auth_in_taiga.static_text import CHOISE_STANDARD_TAIGA_DOMAIN, CHOISE_NOT_STANDARD_TAIGA_DOMAIN, STANDARD_AUTH_TYPE, APPLICATION_AUTH_TYPE


def choise_domain_buttons() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
    [CHOISE_STANDARD_TAIGA_DOMAIN, CHOISE_NOT_STANDARD_TAIGA_DOMAIN]
        ], resize_keyboard=True)
    return markup

def choise_auth_type_buttons() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
    [STANDARD_AUTH_TYPE, APPLICATION_AUTH_TYPE]
        ], resize_keyboard=True)
    return markup

