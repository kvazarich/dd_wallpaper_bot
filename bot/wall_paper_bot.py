import io
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


class WallPaperBot:
    def __init__(self, config, photo_producer, photo_processors):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger('bot')
        self.photo_producer = photo_producer
        self.config = config
        self.photo_processors = photo_processors
        self.markup = {
            'next_button': [InlineKeyboardButton("Next", callback_data='next')]
        }
        self.updater = Updater(token=self.config.get('token'), use_context=True)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self._start))
        dispatcher.add_handler(CallbackQueryHandler(self._next, pattern='next'))
        dispatcher.add_error_handler(self.error)

    def _start(self, update, context):
        keyboard = [self.markup['next_button']]
        update.message.reply_text(
            'Привет, этот бот отправляет картинки на индустриальную тему, с логотипом DataData',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def _next(self, update, context):
        keyboard = [self.markup['next_button']]
        chat_id = update.effective_chat.id
        image = self.photo_producer.get_next_photo()
        image = io.BytesIO(image)
        for processor in self.photo_processors:
            image = processor.process(image=image)
        context.bot.sendPhoto(chat_id=chat_id, photo=image)
        update.callback_query.answer()
        context.bot.sendMessage(
            chat_id=chat_id,
            text='Чтобы получить следующее фото нажмите "Next"',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    def run_bot(self):
        self.updater.start_polling()
        self.updater.idle()
