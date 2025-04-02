import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TimedOut, NetworkError
from dotenv import load_dotenv
from httpx import Timeout

load_dotenv()

# Replace with your actual web app URL
WEB_APP_URL = os.getenv('WEB_APP_URL')

# Configure timeout settings
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
    """Handle errors caused by updates."""
    try:
        if isinstance(context.error, TimedOut):
            print(f"Request timed out: {context.error}")
            # Retry the update if possible
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
    # Configure the application with custom settings
    application = (
        Application.builder()
        .token(os.getenv('TELEGRAM_BOT_TOKEN'))
        .connect_timeout(20.0)  # Increase connection timeout
        .read_timeout(20.0)     # Increase read timeout
        .write_timeout(20.0)    # Increase write timeout
        .pool_timeout(20.0)     # Increase pool timeout
        .build()
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Run the bot with graceful shutdown
    try:
        print("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"Error running bot: {e}")
    finally:
        print("Bot stopped")

if __name__ == '__main__':
    main() 
