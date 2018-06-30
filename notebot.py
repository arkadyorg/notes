import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup

PROXY = settings.PROXY

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



FIRST = range(4)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    mybot = Updater(settings.TELEGRAM_API_KEY, request_kwargs=PROXY)
    dp = mybot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user)],

        states={
            FIRST: [CommandHandler('openbook', booklist),
            CommandHandler('newbook', newbook),
            CommandHandler('deletebook', deletebook),
            CommandHandler('home', greet_user)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update):
    reply_keyboard = [['/openbook', '/newbook', '/deletebook'],
    ['/home']]
    update.message.reply_text(
        'Hi! Nice to seen you, {} what shold we do?'.format(update.message.chat.username),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    logging.info('Chatting with {}'.format(update.message.chat.username))
    return FIRST


def booklist(bot, update):
    user_text = 'here ist the list of your books'
    update.message.reply_text(user_text)


def newbook(bot, update):
    user_text = 'here I ask you how do we call it'
    update.message.reply_text(user_text)

def deletebook(bot, update):
    user_text = 'here I ask what we delete'
    update.message.reply_text(user_text)

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

if __name__ == "__main__":
    logging.info('Bot started')
    main()