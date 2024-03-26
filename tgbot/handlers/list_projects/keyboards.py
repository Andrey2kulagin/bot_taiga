from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.list_projects.static_text import AUTH_BUTTON, CREATE_ISSUE_BUTTON, severity_variants, priority_variants, type_variants


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

def select_project_keyboard(projects) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [str(i + 1) for i in range(len(projects))]
    ], resize_keyboard=True)
    return markup

def select_project_action() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [CREATE_ISSUE_BUTTON]
    ], resize_keyboard=True)
    return markup

def select_issue_severity_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        severity_variants
    ], resize_keyboard=True)
    return markup

def select_issue_priority_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        priority_variants
    ], resize_keyboard=True)
    return markup

def select_issue_type_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        type_variants
    ], resize_keyboard=True)
    return markup
