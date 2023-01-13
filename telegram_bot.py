from loguru import logger
import cv2

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from chart_th import draw_chart

logger.info('Telegram bot polling...')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Initialized...")
    await update.message.reply_text("Initialized...")


async def send_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("sending picture...")
    await update.message.reply_photo(photo=open(func_send_picture(), "rb"))


async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("sending chart...")
    await update.message.reply_photo(photo=open(func_send_chart(), "rb"))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"user {update.message.from_user.first_name} {update.message.from_user.last_name} say {update.message.text}"
    )


def func_send_picture() -> str:
    picpath = "capture.jpg"
    capture = cv2.VideoCapture(0)
    return_value, image = capture.read()
    cv2.imwrite(picpath, image)
    del capture
    return picpath


def func_send_chart() -> str:
    if draw_chart(hours=96, tu="1H", filename="chart.png"):
        return "chart_th.png"
    else:
        return False


def main() -> None:
    """Register handlers and start Bot"""

    # Bot initialization
    application = ApplicationBuilder().token("5695082717:AAESRDnBZ9hTOTdSnkB-ZFce_YayldkNBZY").build()

    # Commands handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("picture", send_picture))
    application.add_handler(CommandHandler("chart", send_chart))

    # Non-commands messages
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=echo))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
