"""Telegram bot polling

Async telegram interface for Telegram Bot Api based on
https://pypi.org/project/python-telegram-bot/

Main functions:
- send_picture -> take a picture using take_a_pic.py
- send_chart -> chart ddbb and send it using chart_th.py
- send_adafruit_dht_data -> Current temperature and humidity from adafruit_dht (or demo dht) to string. 
"""
import os
from datetime import datetime
from functools import wraps
from loguru import logger
import dotenv

from telegram import Update, Bot
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from kweed_utils.take_a_pic import capture
from kweed_utils.chart_th import draw_chart


# Import adafruit_dht on Raspberry PI or a fake number generator
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
if os.getenv("ISRPI") == "yes":
    import kweed_utils.getth as getth
else:
    import kweed_utils.getth_sim as getth


logger.info("Telegram bot polling...")


def send_action(action):
    """
    Sends `action` while processing func command.
    https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#working-with-files-and-media
    """

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Initialized...")
    await update.message.reply_text("Initialized...")


@send_action(ChatAction.UPLOAD_PHOTO)
async def send_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("sending picture...")
    await update.message.reply_photo(photo=open(func_send_chart(), "rb"))


@send_action(ChatAction.TYPING)
async def send_adafruit_dht_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("sending temperature and humidity data as text")
    await update.message.reply_text(text=get_temphumi_str(), parse_mode="HTML")


@send_action(ChatAction.UPLOAD_DOCUMENT)
async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("sending chart...")
    await update.message.reply_photo(photo=open(func_send_chart(), "rb"))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"user {update.message.from_user.first_name} {update.message.from_user.last_name} say {update.message.text}"
    )


def func_send_chart() -> str:
    return draw_chart(hours=48, tu="1H", filename="chart.png")


def func_send_picture() -> str:
    return capture(os.path.join(os.path.dirname(__file__)), 'images', 'capture.jpg')


def get_temphumi_str():
    t = getth.get_temp()
    h = getth.get_humi()
    result = (
        f"Device time: <b>{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}</b>\n"
        f"Temperature: <b>{t}</b> C°\n"
        f"Humidity: <b>{h}</b> %\n"
    )
    return result


def main() -> None:
    """Register handlers and start Bot"""

    # Bot initialization
    application = ApplicationBuilder().token("5695082717:AAESRDnBZ9hTOTdSnkB-ZFce_YayldkNBZY").build()

    # Commands handlers
    application.add_handler(CommandHandler("picture", send_picture))
    application.add_handler(CommandHandler("measure", send_adafruit_dht_data))
    application.add_handler(CommandHandler("chart", send_chart))
    

    # Non-commands messages
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=echo))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
