from datetime import timedelta

from django.utils.timezone import now
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import (
    Dispatcher,
    MessageHandler,
    ConversationHandler, CallbackQueryHandler, CallbackContext, CommandHandler
)
from telegram.ext.filters import Filters
from tgbot.handlers.user_auth_in_taiga import static_text
from tgbot.handlers.admin.utils import _get_csv_from_qs_values
from tgbot.handlers.utils.decorators import admin_only, send_typing_action
from users.models import User
from tgbot.handlers.onboarding.static_text import AUTH_BUTTON
from tgbot.handlers.user_auth_in_taiga.static_text import CHOISE_STANDARD_TAIGA_DOMAIN, CHOISE_NOT_STANDARD_TAIGA_DOMAIN, INPUT_YOUR_DOMAIN, CHOISE_AUTH_TYPE, STANDARD_AUTH_TYPE, APPLICATION_AUTH_TYPE
from tgbot.handlers.user_auth_in_taiga.keyboards import choise_domain_buttons, choise_auth_type_buttons
from tgbot.handlers.onboarding import handlers as onboarding_handlers
import re
DOMAIN_SELECTION, SELF_DOMAIN_INPUT, SEND_AUTH_LINK = range(3)

def login_start_msg(update: Update, context: CallbackContext):
    print("login_start_msg")
    text = static_text.CHOISE_DOMAIN_OFFER
    update.message.reply_text(text=text,
                              reply_markup=choise_domain_buttons())
    return DOMAIN_SELECTION

def standard_domain_handler(update: Update, context: CallbackContext):
    print("standard_domain_handler")
    update.message.reply_text(text="standard_domain_hanler")

def user_domain_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text=INPUT_YOUR_DOMAIN, reply_markup=ReplyKeyboardRemove())
    return SELF_DOMAIN_INPUT

def user_auth_select_type_link_handler(update: Update, context: CallbackContext):

    user_domain = update.message.text
    context.user_data['domain'] = user_domain
    update.message.reply_text(text=f"{CHOISE_AUTH_TYPE}", reply_markup=choise_auth_type_buttons())


user_auth_handler = ConversationHandler(
                entry_points=[
                    MessageHandler(Filters.regex(rf"^{AUTH_BUTTON}$"), login_start_msg),
                ],
                states={
                    DOMAIN_SELECTION: [
                        MessageHandler(Filters.regex(fr"^{re.escape(CHOISE_STANDARD_TAIGA_DOMAIN)}$"), standard_domain_handler),
                        MessageHandler(Filters.regex(rf"^{re.escape(CHOISE_NOT_STANDARD_TAIGA_DOMAIN)}$"),user_domain_handler),
                    ],
                    SELF_DOMAIN_INPUT: [
                        MessageHandler(Filters.text & ~Filters.command, user_auth_select_type_link_handler),
                        MessageHandler(Filters.regex(rf"^{re.escape(STANDARD_AUTH_TYPE)}$"),user_domain_handler),
                        MessageHandler(Filters.regex(rf"^{re.escape(CHOISE_NOT_STANDARD_TAIGA_DOMAIN)}$"),user_domain_handler),
                        MessageHandler(Filters.regex(rf"^{re.escape(APPLICATION_AUTH_TYPE)}$"),user_domain_handler),
                    ],
                    #manage_data.DIAG_WAIT_START_STATE: [
                    #    MessageHandler(Filters.regex(rf"^{BACK_TO_MAIN_MENU_TEXT}$"), diag_back_to_main_menu_handler),
                    #    MessageHandler(Filters.regex(rf"^{BACK_TO_PREVIOUS_STEP_TEXT}$"), diag_to_current_page_handler),
                    #    MessageHandler(Filters.regex(rf"^{DIAG_START_BUTTON_TEXT}$"), diag_start_topic_handler),
                    #],
                    
                },
                fallbacks=[]
            )

