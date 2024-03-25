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
# TODO: посмотреть нужен ли здесь -> None
def command_projects(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    if u.is_taiga_auth:
        # do stuff to show project list (call the backend util to do so)
        # call list projects and give it tg user id
        tg_id = update.message.from_user.id
        projects = utils.get_projects(tg_id)
        text = utils.format_projects(projects)
        update.message.reply_text(text=text, reply_markup=select_project(projects))
        return PROJECT_SELECTION
    else:
        # say to authorize
        text = static_text.bot_user_not_authorized.format(first_name=u.first_name)
        update.message.reply_text(text=text,
                                  reply_markup=make_keyboard_for_start_command())
        return dispatcher.AUTH_USER


def create_issue(update: Update, context: CallbackContext):
    # получаем предыдущее сообщение от пользователя - оно скорее всего содержит двузначное число - индекс проекта в списке проектов
    project_number = int(update.message.from_user) - 1
    tg_id = update.message.from_user.id
    # список проектов, вернувшийся с сервера
    # [{"id": 1127272, "name": "our bot"}, {"id": 1052184, "name": "Test"}, {"id": 1059926, "name": "Test project"}]
    projects = utils.get_projects(tg_id)
    # id выбранного проекта. Выбираем нужный объект по счету из массива, а из него уже id проекта
    # 1127272
    selected_project_id = projects[project_number]['id']
    '''
    тут будут вызываться отдельные функции, которые будут спрашивать у пользователя по аргументу для 
    bot_taiga/utils/taiga_back/create_issue.reate_issue
    аргументы:
        "description": description,  # string, описание issue - спросить у пользователя
        "is_closed": is_closed,
        "priority": priority,  # id приоритета                - спросить у пользователя
        "project": project,  # id проекта                     - спросили
        "severity": severity,  # id серьёзности               - спросить у пользователя
        "status": status,  # id статуса                       - наверное самому задавать
        "subject": subject,  # название issue                 - спросить у пользователя
        "tags": tags,  # лист тегов
        "type": type  # id тайпа
    проблема в том, как передавать от одной функции к другой это все
    надо както использовать стейты при этом
    может быть можно писать это все в дб, но звучит не очень
    заставить висеть ЭТУ функцию, пока пользователь не прокликает все остальные функции для получения
    от него аргументов - такая себе затея, учитывая что у нас асинхронный клиент
    '''

projects_menu_handler = ConversationHandler(
    entry_points = [CommandHandler("projects", command_projects)],
    states={
        PROJECT_SELECTION: [
            # ([1-9]|[1-9][0-9])
                MessageHandler(Filters.regex('[1-9]|[1-9][0-9]'), create_issue),
        ],
        NAMING_ISSUE: [],
    }
)