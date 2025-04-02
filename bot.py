import os

from dotenv import load_dotenv
from httpx import Timeout
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TimedOut, NetworkError
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

WEB_APP_URL = os.getenv('WEB_APP_URL')

REQUEST_TIMEOUT = Timeout(connect=20.0, read=20.0, write=20.0, pool=20.0)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Генерировать изображение", web_app={"url": WEB_APP_URL})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в генератор изображений Stable Diffusion! Нажмите кнопку ниже, чтобы начать создавать изображения.",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Please use the web app to generate images!")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if isinstance(context.error, TimedOut):
            print(f"Request timed out: {context.error}")
            if update and update.message:
                await update.message.reply_text(
                    "Sorry, the request timed out. Please try again."
                )
        elif isinstance(context.error, NetworkError):
            print(f"Network error occurred: {context.error}")
            if update and update.message:
                await update.message.reply_text(
                    "Sorry, a network error occurred. Please try again later."
                )
        else:
            print(f"Error occurred: {context.error}")
    except Exception as e:
        print(f"Error in error handler: {e}")


def main():
    application = (
        Application.builder()
        .token(os.getenv('TELEGRAM_BOT_TOKEN'))
        .connect_timeout(20.0)
        .read_timeout(20.0)
        .write_timeout(20.0)
        .pool_timeout(20.0)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.add_error_handler(error_handler)

    try:
        print("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"Error running bot: {e}")
    finally:
        print("Bot stopped")


if __name__ == '__main__':
    main()
