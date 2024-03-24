import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

from tgbot.handlers.list_projects import static_text, utils, static_text
from users.models import User
from tgbot.handlers.list_projects.keyboards import make_keyboard_for_start_command, select_project
from tgbot import dispatcher


# Коллбек команды списка проектов. Если пользователь уже входил в тайгу через бота, будет выведен список проектов
# если не авторизован, то попросим авторизоваться
def command_projects(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    if u.is_taiga_auth:
        # do stuff to show project list (call the backend util to do so)
        # call list projects and give it tg user id
        tg_id = update.message.from_user.id
        projects = utils.format_projects(utils.get_projects(tg_id))
        text = ""
        update.message.reply_text(text=projects, reply_markup=select_project(utils.get_projects(tg_id)))
    else:
        # say to authorize
        text = static_text.bot_user_not_authorized.format(first_name=u.first_name)
        update.message.reply_text(text=text,
                                  reply_markup=make_keyboard_for_start_command())
        return dispatcher.AUTH_USER
