import os
import configparser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        raise FileNotFoundError('Не найден файл конфигурации {}'.format(path))

    _config = configparser.ConfigParser()
    _config.read(path)
    return _config


def start(update, context):
    update.message.reply_text('Привет, этот бот отправляет картинки на индустриальную тему, с логотипом DataData')


def run_bot(bot_config):
    updater = Updater(token=bot_config.get('token'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    config = get_config('config.ini')
    run_bot(dict(config.items('bot_config')))
