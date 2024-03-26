import datetime

from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters, ContextTypes

from tgbot.handlers.list_projects import static_text, utils
from tgbot.handlers.list_projects.static_text import select_project_action_message, CREATE_ISSUE_BUTTON, name_issue_message, describe_issue_message, select_issue_severity_message, select_issue_priority_message, select_issue_type_message, type_variants, priority_variants, severity_variants
from users.models import User
from tgbot.handlers.list_projects.keyboards import make_keyboard_for_start_command, select_project_keyboard, select_project_action, select_issue_severity_keyboard, select_issue_priority_keyboard, select_issue_type_keyboard
from tgbot import dispatcher
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from utils.taiga_back.create_issue import create_issue
import re
PROJECT_SELECTION, NAMING_ISSUE, DESCRIBING_ISSUE, SELECTING_SEVERITY, SELECTING_PRIORITY, SELECTING_TYPE, CREATING_ISSUE = range(7)

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
        print(projects)
        text = utils.format_projects(projects)
        update.message.reply_text(text=text, reply_markup=select_project_keyboard(projects))
        return PROJECT_SELECTION
    else:
        # say to authorize
        text = static_text.bot_user_not_authorized.format(first_name=u.first_name)
        update.message.reply_text(text=text,
                                  reply_markup=make_keyboard_for_start_command())
        return dispatcher.AUTH_USER


def select_project(update: Update, context: CallbackContext):
    # TODO: обнулить юзердату здесь (касаемо создания issue)
    # получаем предыдущее сообщение от пользователя - оно скорее всего содержит двузначное или однозначное
    # число - индекс проекта в списке проектовContextTypes.DEFAULT_TYPE
    # "1"
    # print(update.message.text, type(update.message.text))
    project_number = int(update.message.text) - 1
    tg_id = update.message.from_user.id
    # список проектов, вернувшийся с сервера
    # [{"id": 1127272, "name": "our bot"}, {"id": 1052184, "name": "Test"}, {"id": 1059926, "name": "Test project"}]
    projects = utils.get_projects(tg_id)
    # id выбранного проекта. Выбираем нужный объект по счету из массива, а из него уже id проекта
    # 1127272
    selected_project_id = projects[project_number]['id']
    # запоминаем в контест id проекта
    context.user_data["selected_project_id"] = str(selected_project_id)
    update.message.reply_text(text=select_project_action_message, reply_markup=select_project_action())
    return NAMING_ISSUE
    '''
    тут будут вызываться отдельные функции, которые будут спрашивать у пользователя по аргументу для 
    bot_taiga/utils/taiga_back/select_project.reate_issue
    аргументы:
        "description": description,  # string, описание issue - спросить у пользователя
        "is_closed": is_closed,
        "priority": priority,  # id приоритета                - спросить у пользователя
        "project": project,  # id проекта                     - спросили
        "severity": severity,  # id серьёзности               - спросить у пользователя
        "status": status,  # id статуса                       - наверное самому задавать
        "subject": subject,  # название issue                 - спросить у пользователя
        "tags": tags,  # лист тегов
        "type": type  # id тайпа                              - cпросить у пользователя
    передавать это всё надо через контекст
    https://docs.python-telegram-bot.org/en/stable/telegram.ext.callbackcontext.html (смотрим на тип контекста user_data)
    https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py (пример)
    '''

# говорим пользователю написать название, перекидываем на следующий стейт где запомним его
def name_issue(update: Update, context: CallbackContext):
    print(context.user_data["selected_project_id"])
    update.message.reply_text(text=name_issue_message, reply_markup=ReplyKeyboardRemove())
    return DESCRIBING_ISSUE

def describe_issue(update: Update, context: CallbackContext):
    issue_name = str(update.message.text)
    context.user_data["issue_name"] = issue_name
    text = describe_issue_message + ' "' + issue_name + '".'
    update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
    return SELECTING_SEVERITY

def select_issue_severity(update: Update, context: CallbackContext):
    issue_description = str(update.message.text)
    context.user_data["issue_description"] = issue_description
    update.message.reply_text(text=select_issue_severity_message, reply_markup=select_issue_severity_keyboard())
    return SELECTING_PRIORITY

def select_issue_priority(update:Update, context: CallbackContext):
    issue_severity = str(update.message.text)
    context.user_data["issue_severity"] = issue_severity
    update.message.reply_text(text=select_issue_priority_message, reply_markup=select_issue_priority_keyboard())
    return SELECTING_TYPE

def select_issue_type(update:Update, context: CallbackContext):
    issue_priority = str(update.message.text)
    context.user_data["issue_priority"] = issue_priority
    update.message.reply_text(text=select_issue_type_message, reply_markup=select_issue_type_keyboard())
    return CREATING_ISSUE

def create_issue_command_handler(update:Update, context: CallbackContext):
    tg_id = update.message.from_user.id
    issue_type = str(update.message.text)
    issue_priority = str(context.user_data["issue_priority"])
    issue_severity = str(context.user_data["issue_severity"])
    issue_description = str(context.user_data["issue_description"])
    issue_name = str(context.user_data["issue_name"])
    project_id = int(context.user_data["selected_project_id"])
    print(project_id, issue_name, issue_priority, issue_severity, issue_description)
    # TODO: Убрать все что ниже в utils
    # замена типов issue на цифровые
    if issue_type == type_variants[0]:
        issue_type = 3391300
    elif issue_type == type_variants[1]:
        issue_type = 3391301
    elif issue_type == type_variants[2]:
        issue_type = 3391302

    # замена приоритетов на цифровые
    if issue_priority == priority_variants[0]:
        issue_priority = 3384695
    elif issue_priority == priority_variants[1]:
        issue_priority = 3384696
    elif issue_priority == priority_variants[2]:
        issue_priority = 3384697

    # замена важности на цифровую
    if issue_severity == severity_variants[0]:
        issue_severity = 5633959
    elif issue_severity == severity_variants[1]:
        issue_severity = 5633960
    elif issue_severity == severity_variants[2]:
        issue_severity = 5633961
    elif issue_severity == severity_variants[3]:
        issue_severity = 5633962
    elif issue_severity == severity_variants[4]:
        issue_severity = 5633963
    
    
    create_issue(
        auth_token=utils.get_taiga_token_by_tg_id(tg_id),
        description=issue_description,
        priority=issue_priority,
        project=project_id,
        severity=issue_severity,
        subject=issue_name,
        type=issue_type
    )
    # TODO: исправить на статический текст
    update.message.reply_text(text="Готово", reply_markup=ReplyKeyboardRemove())
    return -1

projects_menu_handler = ConversationHandler(
    entry_points = [CommandHandler("projects", command_projects)],
    states={
        PROJECT_SELECTION: [
            # ([1-9]|[1-9][0-9])
            MessageHandler(Filters.regex('[1-9]|[1-9][0-9]'), select_project),
        ],
        NAMING_ISSUE: [
            MessageHandler(Filters.regex(rf"^{re.escape(CREATE_ISSUE_BUTTON)}$"), name_issue)
        ],
        # TODO: придумать защиту от XSS
        DESCRIBING_ISSUE: [
            MessageHandler(Filters.text, describe_issue)
        ],
        SELECTING_SEVERITY: [
            MessageHandler(Filters.text, select_issue_severity)
        ],
        # TODO: проверять нажата ли кнопка или текст от балды
        SELECTING_PRIORITY: [
            MessageHandler(Filters.text, select_issue_priority)
        ],
        # TODO: проверять нажата ли кнопка или текст от балды
        SELECTING_TYPE: [
            MessageHandler(Filters.text, select_issue_type)
        ],
        # TODO: проверять нажата ли кнопка или текст от балды
        CREATING_ISSUE: [
            MessageHandler(Filters.text, create_issue_command_handler)
        ]
    },
    fallbacks = [CommandHandler('abort', command_projects)]
)