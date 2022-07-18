TOKEN = "5513769814:AAHUy7Wkwjym9D_uoztNBSDcPcf79u3Wf3s"

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext
import logging
from Fetcher.fetcher import Fetcher

logging.basicConfig(format='%(levelname)s - %(message)s',
                     level=logging.DEBUG)
logger = logging.getLogger(__name__)
updater = None

def sheet_update(command: str):
    print("req !")
    command = command.strip()
    if len(command) != 0:
        if command == "NIVITO_KEYWORDS":
            print("updating urls keywords")
            fetcher.update()
        if command == "NIVITO_KEYWORDS_DATA":
            print("loading data ")
            fetcher.load_data()
    
def echo(update: Update, context: CallbackContext):
    print(update)
    if "channel_post" in update.to_dict().keys():

        if update.channel_post.text.startswith("/sheet_update"):
            sheet_update(update.channel_post.text[13:])

def start_bot():
    global updater
    global fetcher

    fetcher = Fetcher()
    updater = Updater(
        TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text,echo))


    updater.start_polling()
    updater.idle()
