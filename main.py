import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram.ext import ApplicationBuilder, MessageHandler, filters

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

async def echo(update, context):
    text = update.message.text
    # Yahan apni Gemini API call lagayein jo pehle likhi thi
    await update.message.reply_text(f"Aapne kaha: {text}")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
    
