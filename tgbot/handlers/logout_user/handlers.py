import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters
from tgbot.handlers.logout_user import static_text
from tgbot.handlers.logout_user.utils import delete_user
from users.models import User
from tgbot.handlers.logout_user.keyboards import start_keyboard
from tgbot import dispatcher


def command_logout(update: Update, context: CallbackContext) -> int:
    u, created = User.get_user_and_created(update, context)
    if u.is_taiga_auth:
        tg_id = update.message.from_user.id
        delete_user(tg_id)
        text = static_text.logout_text
        update.message.reply_text(text=text, reply_markup=start_keyboard())
        return -1
