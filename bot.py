import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load your Telegram token from Railway environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user when they send /start."""
    await update.message.reply_text("Hello! Ask me any question, and I will answer it instantly.")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Takes the question, asks Pollinations AI, and replies."""
    user_message = update.message.text
    
    # Show that the bot is thinking/typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # We send the question directly to the free, keyless text API
        # We use standard URL encoding to safely send the text
        url = f"https://text.pollinations.ai/{requests.utils.quote(user_message)}"
        
        # Make the request to get the AI text response
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Sorry, I'm having trouble thinking of an answer right now.")
            
    except Exception as e:
        logging.error(f"Error getting AI response: {e}")
        await update.message.reply_text("Sorry, I encountered an internal error trying to answer that.")

if __name__ == '__main__':
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN variable is missing!")
        exit(1)
        
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    
    logging.info("Starting bot on keyless setup...")
    app.run_polling()
