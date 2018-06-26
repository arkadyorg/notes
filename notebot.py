import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup

PROXY = settings.PROXY

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

#CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['/mybooks', '/newbook'],
                  ['/openbook', '/deletebook', '/renamebook'],
                  ['/whoami']]
bookmarkup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

poop=0


def main():
    mybot = Updater(settings.TELEGRAM_API_KEY, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("whoami", userinfo))

    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update):
    text = """
Oh hi!
That's one small step for notesbot, one giant leap for //project_name//
/start

			"""
    logging.info('Chatting with {}'.format(update.message.chat.username))
    update.message.reply_text(text,reply_markup=bookmarkup)


def userinfo(bot, update):
    user_text = 'You are {} with id {}'. format(update.message.chat.username, update.message.chat.id)
    print(user_text)
    print(update)
    update.message.reply_text(user_text)

if __name__ == "__main__":
    logging.info('Bot started')
    main()