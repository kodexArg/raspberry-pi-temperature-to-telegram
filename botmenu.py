# Loggin...
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Imports...
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Initialized...")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"user {update.message.from_user.first_name} {update.message.from_user.last_name} say {update.message.text}")


def main() -> None:
    """Register handlers and start Bot"""

    # Bot initialization
    application = ApplicationBuilder().token("5695082717:AAESRDnBZ9hTOTdSnkB-ZFce_YayldkNBZY").build()

    # Commands handlers
    application.add_handler(CommandHandler("start", start))

    # Non-commands messages
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=echo))

    #Start the bot
    application.run_polling()



if __name__ == "__main__":
    main()
    
