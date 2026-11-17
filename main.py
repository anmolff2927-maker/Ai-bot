import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from openai import OpenAI

# Render ke liye dummy web server taki port error na aaye
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Server ko alag thread mein chalayein
threading.Thread(target=run_server, daemon=True).start()

# OpenAI client setup (OpenAI API key env variable se uthayega)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# /start command ka handler
async def start(update, context):
    await update.message.reply_text("Namaste! Main Xyren AI hoon (Powered by ChatGPT). Aap mujhse kuch bhi pooch sakte hain!")

# Text messages (ChatGPT AI) ka handler
async def handle_message(update, context):
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f"Error details: {str(e)}")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers add karna
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
    
