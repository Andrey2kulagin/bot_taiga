from tgbot.main import bot
from users.models import User
from telegram import ParseMode


def send_notification_message(taiga_id, text):
    try:
        user = User.objects.get(taiga_id=taiga_id)
        tg_id = user.user_id
        bot.send_message(chat_id=tg_id, text=text, parse_mode=ParseMode.MARKDOWN)
    except User.DoesNotExist:
        print("Такой пользователь не зарегистрирован в боте, письма не пишем")