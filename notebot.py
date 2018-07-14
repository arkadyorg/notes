import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup
from booklogic import new_book, book_list, delete_book, new_book_page, page_list, drop_page
from emoji import emojize

PROXY = settings.PROXY

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

GET_BOOK_TITLE, DELETE_BOOK_TITLE, NEW_PAGE_HEADING, NEW_PAGE_TEXT, BOOK_SELECTOR, PAGE_LISTER = range(6)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def greet_user(bot, update):
    reply_keyboard = [['/booklist', '/newbook', '/deletebook'],
    ['/newpage','/pagelist','/deletepage'],
    ['/start','/cancel']]
    update.message.reply_text(
        'Hi! Nice to see you, {} what shold we do?'.format(update.message.chat.username),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    logging.info('Strrted chatting with {}'.format(update.message.chat.username))


def booklist(bot, update):
    user_text = str(book_list(update.message.chat.id))
    update.message.reply_text(user_text)
    logging.info('Catch booklist command from {}'.format(update.message.chat.username))


def newbook(bot, update):
    user_text = 'Please enter the book name'
    update.message.reply_text(user_text)
    logging.info('Catch newbook command from {}'.format(update.message.chat.username))

    return GET_BOOK_TITLE

def book_title(bot,update):
    nbook_name = update.message.text
    uid=update.message.chat.id
    new_book(nbook_name,uid)
    logging.info('Created book with title {}'.format(update.message.text))
    return ConversationHandler.END 

def deletebook(bot, update):
    user_text = 'Which book number should I delete?'
    update.message.reply_text(user_text)
    logging.info('Catch deletebook command from {}'.format(update.message.chat.username))
    return DELETE_BOOK_TITLE

def deletebook_id(bot, update):
    rem_id = update.message.text
    delete_book(rem_id)
    logging.info('Deleted book with id {}'.format(update.message.text))
    return ConversationHandler.END 


def newpage(bot, update, user_data):
    user_text = 'How would we call our page?'
    update.message.reply_text(user_text)
    logging.info('Catch newpage command from {}'.format(update.message.chat.username))
    return NEW_PAGE_HEADING

def page_title(bot,update, user_data):
    user_text = 'What text should be there?'
    title = update.message.text
    user_data['title'] = update.message.text
    update.message.reply_text(user_text)
    logging.info('Catch page_title command from {}'.format(update.message.chat.username))
    return NEW_PAGE_TEXT

def page_text(bot,update,user_data):
    user_text = 'Where should I add it? {}'.format(str(book_list(update.message.chat.id)))
    user_data['text'] = update.message.text
    update.message.reply_text(user_text)
    logging.info('Catch page_text command from {}'.format(update.message.chat.username))
    return BOOK_SELECTOR 

def book_selector(bot,update,user_data):
    user_data['book'] = update.message.text
    new_book_page(user_data['book'],user_data['title'],user_data['text'])
    user_text = emojize(':rocket: Done')
    update.message.reply_text(user_text)
    logging.info('Catch book_selector command from {}'.format(update.message.chat.username))
    return ConversationHandler.END 

def pagelist(bot, update, user_data):
    user_text = 'Which book would you like to read? {}'.format(str(book_list(update.message.chat.id)))
    update.message.reply_text(user_text)
    logging.info('Catch page_list command from {}'.format(update.message.chat.username))
    return PAGE_LISTER

def page_show(bot, update,user_data):
    user_text = str(page_list(update.message.text))
    update.message.reply_text(user_text)
    logging.info('Catch page_show command from {}'.format(update.message.chat.username))
    return ConversationHandler.END 


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Bye! I hope we can talk again some day.')
    logging.info('Catch cancel command from {}'.format(update.message.chat.username))
    return ConversationHandler.END
###*
def deletepage(bot, update, user_data):
    user_text = 'From which book should I delete the page? {}'.format(str(book_list(update.message.chat.id)))
    update.message.reply_text(user_text)
    logging.info('Catch deletepage command from {}'.format(update.message.chat.username))
    return BOOK_SELECTOR    

def dp_book_selector(bot, update, user_data):
    user_data['bookid'] = update.message.text
    user_text = 'Which page number would you like to drop?{}'.format(str(page_list(user_data['bookid'])))
    title = update.message.text
    update.message.reply_text(user_text)
    logging.info('Catch dp_book_selector command from {}'.format(update.message.chat.username))    
    return PAGE_LISTER

def dp_page_selector(bot, update, user_data):
    user_data['pagenum'] = update.message.text
    drop_page(user_data['bookid'],user_data['pagenum'])
    user_text = emojize(':rocket: Done')
    update.message.reply_text(user_text)
    logging.info('Catch dp_page_selector command from {}'.format(update.message.chat.username))
    return ConversationHandler.END 


###*
def main():
    mybot = Updater(settings.TELEGRAM_API_KEY, request_kwargs=PROXY)
    dp = mybot.dispatcher
#############################################################
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newbook', newbook)],
            states={
            GET_BOOK_TITLE: [MessageHandler(Filters.text, book_title)]          
                    },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)


    conv_handler_delete = ConversationHandler(
            entry_points=[CommandHandler('deletebook', deletebook)],
            states={
            DELETE_BOOK_TITLE: [MessageHandler(Filters.text, deletebook_id)]          
                    },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler_delete)

    nw_page_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('newpage', newpage, pass_user_data=True)],
            states={
            NEW_PAGE_HEADING: [MessageHandler(Filters.text, page_title, pass_user_data=True)],
            NEW_PAGE_TEXT: [MessageHandler(Filters.text, page_text, pass_user_data=True)],
            BOOK_SELECTOR: [MessageHandler(Filters.text, book_selector, pass_user_data=True)]         
                    },
        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
    dp.add_handler(nw_page_conv_handler)

    page_list_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('pagelist', pagelist, pass_user_data=True)],
            states={
            PAGE_LISTER: [MessageHandler(Filters.text, page_show, pass_user_data=True)]         
                    },
        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
    dp.add_handler(page_list_conv_handler)

    page_drop_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('deletepage', deletepage, pass_user_data=True)],
            states={
            BOOK_SELECTOR: [MessageHandler(Filters.text, dp_book_selector, pass_user_data=True)],
            PAGE_LISTER: [MessageHandler(Filters.text, dp_page_selector, pass_user_data=True)]           
                    },
        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
    dp.add_handler(page_drop_conv_handler)

#############################################################
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('booklist', booklist))
    dp.add_handler(CommandHandler('home', greet_user))

    # log all errors
    dp.add_error_handler(error)
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    logging.info('Bot started')
    main()