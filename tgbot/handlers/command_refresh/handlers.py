from telegram import Update
from telegram.ext import CallbackContext
from tgbot.handlers.command_refresh import static_text
from utils.taiga_back.refresh_token import refresh_access_token
from utils.taiga_back.get_taiga_token import get_taiga_token_by_tg_id


def refresh_token(update: Update, context: CallbackContext) -> None:
    tg_id = update.message.from_user.id
    text = refresh_access_token(tg_id)[1]
    update.message.reply_text(text=text)
