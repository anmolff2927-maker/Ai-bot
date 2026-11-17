import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from google import genai

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

# Gemini client setup
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

async def handle_message(update, context):
    user_message = update.message.text
    try:
        # Gemini se response lena
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Bhai, kuch error aa gaya hai API call mein!")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
    
