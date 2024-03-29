from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.onboarding.static_text import AUTH_BUTTON


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
    [AUTH_BUTTON]
        ], resize_keyboard=True)
    return markup

def make_keyboard_for_projects_list() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [AUTH_BUTTON]
    ], resize_keyboard=True)
    return markup

def select_project(projects) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [str(i + 1) for i in range(len(projects))]
    ], resize_keyboard=True)
    return markup
