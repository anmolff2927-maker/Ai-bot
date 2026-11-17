import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# 1. Render ke liye dummy web server jo port active rakhega
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Web server ko background thread mein start karein
threading.Thread(target=run_server, daemon=True).start()

# 2. Telegram Bot ka message handler (Gemini ke sath)
async def echo(update, context):
    text = update.message.text
    await update.message.reply_text(f"Aapne kaha: {text}")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable missing!")
        return
        
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot polling shuru ho rahi hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
