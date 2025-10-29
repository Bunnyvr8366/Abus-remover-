import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8430889974:AAF4x_EdS5-7UlxT6cj53lR-K15JXThVw58"

# List of abusive words (lowercase)
ABUSIVE_WORDS = [
    "mc", "bc", "lavdya",  # replace with your words
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ I'm your chat filter bot. I delete abusive messages after a short delay.")

async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if any(word in text for word in ABUSIVE_WORDS):
        delay = random.randint(10, 15)  # random delay between 10–15 seconds
        warn_msg = await update.message.reply_text(
            f"⚠️ This message will be deleted in {delay} seconds due to abusive content.",
            quote=True
        )

        try:
            await asyncio.sleep(delay)
            await update.message.delete()
            await warn_msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    print("Filter bot running...")
    app.run_polling()