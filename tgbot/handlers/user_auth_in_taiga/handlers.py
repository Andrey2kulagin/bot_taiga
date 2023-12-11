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
from tgbot.handlers.user_auth_in_taiga.static_text import (CHOISE_STANDARD_TAIGA_DOMAIN, CHOISE_NOT_STANDARD_TAIGA_DOMAIN, INPUT_YOUR_DOMAIN,
                                                            CHOISE_AUTH_TYPE, STANDARD_AUTH_TYPE, APPLICATION_AUTH_TYPE, NOT_VALID_DOMAIN, LINK_FOR_AUTH,
                                                            GENERATE_LINK

                                                            )
from tgbot.handlers.user_auth_in_taiga.keyboards import choise_domain_buttons, choise_auth_type_buttons, reg_link_button
from tgbot.handlers.onboarding import handlers as onboarding_handlers
import re
from tgbot.handlers.utils.login_service import generate_standard_auth_link, generate_application_auth_link
from utils.login.all_service import domain_validate_and_normalize
DOMAIN_SELECTION, SELF_DOMAIN_HANDLER, SEND_AUTH_LINK, SELF_DOMAIN_INPUT = range(4)

def login_start_msg(update: Update, context: CallbackContext):
    print("login_start_msg")
    text = static_text.CHOISE_DOMAIN_OFFER
    update.message.reply_text(text=text,
                              reply_markup=choise_domain_buttons())
    return DOMAIN_SELECTION

def standard_domain_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    print("ТУТА")
    link = generate_standard_auth_link(domain="https://api.taiga.io/", tg_id=user_id)
    update.message.reply_text(text=f"{GENERATE_LINK}", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(text=f"{LINK_FOR_AUTH}",reply_markup=reg_link_button(link))

def user_domain_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text=INPUT_YOUR_DOMAIN, reply_markup=ReplyKeyboardRemove())
    return SELF_DOMAIN_INPUT

def selfhost_domain_input(update: Update, context: CallbackContext):
    user_domain_input = update.message.text
    status, normalize_domain = domain_validate_and_normalize(user_domain_input)
    if status:
        context.user_data['domain'] = normalize_domain
        update.message.reply_text(text=f"{CHOISE_AUTH_TYPE}", reply_markup=choise_auth_type_buttons())
        return SELF_DOMAIN_HANDLER
    else:
        update.message.reply_text(text=f"{NOT_VALID_DOMAIN.format(error=normalize_domain)}")

def selfhost_standard_login_link_gen(update: Update, context: CallbackContext):
    user_domain =  context.user_data['domain']
    user = update.message.from_user
    user_id = user.id
    link = generate_standard_auth_link(domain=user_domain, tg_id=user_id)
    update.message.reply_text(text=f"{GENERATE_LINK}", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(text=f"{LINK_FOR_AUTH}",reply_markup=reg_link_button(link))

def selfhost_application_login_link_gen(update: Update, context: CallbackContext):
    user_domain =  context.user_data['domain']
    user = update.message.from_user
    user_id = user.id
    link = generate_application_auth_link(domain=user_domain, tg_id=user_id)
    update.message.reply_text(text=f"{GENERATE_LINK}", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(text=f"{LINK_FOR_AUTH}",reply_markup=reg_link_button(link))

    


user_auth_handler = ConversationHandler(
                entry_points=[
                    MessageHandler(Filters.regex(rf"^{AUTH_BUTTON}$"), login_start_msg),# входная функция - нажатие кнопки "Авторизация"
                ],
                states={
                    DOMAIN_SELECTION: [# выбор домена
                        MessageHandler(Filters.regex(fr"^{re.escape(CHOISE_STANDARD_TAIGA_DOMAIN)}$"), standard_domain_handler), # Обработка выбора стандартного домена тайги
                        MessageHandler(Filters.regex(rf"^{re.escape(CHOISE_NOT_STANDARD_TAIGA_DOMAIN)}$"),user_domain_handler),# Обработка своего домена
                    ],
                    SELF_DOMAIN_HANDLER: [# Действия по авторизации с селфхост тайгой
                        MessageHandler(Filters.regex(rf"^{re.escape(STANDARD_AUTH_TYPE)}$"),selfhost_standard_login_link_gen),# Обработка нажатия на кнопку по паролю
                        MessageHandler(Filters.regex(rf"^{re.escape(APPLICATION_AUTH_TYPE)}$"),selfhost_application_login_link_gen),# Обработка нажатия на кнопку по токену приложения
                    ],
                    SELF_DOMAIN_INPUT: [# Действия по авторизации с селфхост тайгой
                        MessageHandler(Filters.text & ~Filters.command, selfhost_domain_input),# приём домена непосредственно
                    ],
                    #manage_data.DIAG_WAIT_START_STATE: [
                    #    MessageHandler(Filters.regex(rf"^{BACK_TO_MAIN_MENU_TEXT}$"), diag_back_to_main_menu_handler),
                    #    MessageHandler(Filters.regex(rf"^{BACK_TO_PREVIOUS_STEP_TEXT}$"), diag_to_current_page_handler),
                    #    MessageHandler(Filters.regex(rf"^{DIAG_START_BUTTON_TEXT}$"), diag_start_topic_handler),
                    #],
                    
                },
                fallbacks=[CommandHandler('start', onboarding_handlers.command_start)]
            )

