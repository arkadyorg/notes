import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY = settings.PROXY

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.TELEGRAM_API_KEY, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update):
    text = """
Oh hi!
That's one small step for notesbot, one giant leap for //project_name//

			"""
    logging.info('Chatting with {}'.format(update.message.chat.username))
    update.message.reply_text(text)

if __name__ == "__main__":
    logging.info('Bot started')
    main()