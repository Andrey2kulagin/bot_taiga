import datetime
from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters
from tgbot.handlers.ping_command import static_text, utils, static_text
from users.models import User
from tgbot import dispatcher


# Коллбек команды списка проектов. Если пользователь уже входил в тайгу через бота, будет выведен список проектов
# если не авторизован, то попросим авторизоваться
def ping_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text=static_text.ping_text)
