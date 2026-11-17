import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste bhai! Main tera AI chatbot hoon.\nKuch bhi poochh, main jawab dunga.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Sorry yaar, thodi problem aa gayi. Phir se try kar.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot start ho gaya...")
    app.run_polling()

if __name__ == "__main__":
    main()
