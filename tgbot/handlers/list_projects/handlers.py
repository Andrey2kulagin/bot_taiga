import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

from tgbot.handlers.list_projects import static_text, utils, static_text
from users.models import User
from tgbot.handlers.list_projects.keyboards import make_keyboard_for_start_command
from tgbot import dispatcher


# Коллбек команды списка проектов. Если пользователь уже входил в тайгу через бота, будет выведен список проектов
# если не авторизован, то попросим авторизоваться
def command_projects(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    if u.is_taiga_auth:
        # do stuff to show project list (call the backend util to do so)
        # call list projects and give it tg user id
        tg_id = update.message.from_user.id
        projects = utils.get_projects(tg_id)
        text = ""
        try:
            # for i in range(len(projects[1])):
            #     text += "**" + str(i + 1) + ".** " + projects[1][i]["name"] + "\n"
            # update.message.reply_text(text=text, reply_markup=make_keyboard_for_projects_list())
            update.message.reply_text(text=projects.text())
        except Exception:
            update.message.reply_text(text=static_text.generic_error_message)
    else:
        # say to authorize
        text = static_text.bot_user_not_authorized.format(first_name=u.first_name)
        update.message.reply_text(text=text,
                                  reply_markup=make_keyboard_for_start_command())
        return dispatcher.AUTH_USER
