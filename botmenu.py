# Loggin...
from loguru import logger

# Imports...
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import cv2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Initialized...")


async def take_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_photo(photo=open(func_take_picture(), 'rb'))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"user {update.message.from_user.first_name} {update.message.from_user.last_name} say {update.message.text}")


def func_take_picture():
    logger.warning("I'm trying to take a picture")
    picpath = 'capture.jpg'
    capture = cv2.VideoCapture(0)
    return_value, image = capture.read()
    cv2.imwrite(picpath, image)
    del(capture)
    return picpath
    

def main() -> None:
    """Register handlers and start Bot"""

    # Bot initialization
    application = ApplicationBuilder().token("5695082717:AAESRDnBZ9hTOTdSnkB-ZFce_YayldkNBZY").build()

    # Commands handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("take_picture", take_picture))

    # Non-commands messages
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=echo))

    #Start the bot
    application.run_polling()



if __name__ == "__main__":
    main()
    
