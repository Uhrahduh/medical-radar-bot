import os
import asyncio
import threading
from flask import Flask

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------------- CONFIG ----------------

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN no está configurado en Render")

# ---------------- FLASK ----------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Medical Radar Bot Running"

# ---------------- TELEGRAM HANDLERS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo 🚀")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comandos disponibles: /start")

# ---------------- BOT CORE ----------------

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))

    print("BOT START")

    async def main():
        await application.initialize()
        await application.start()

        # IMPORTANTE: evita conflicto de getUpdates en Render
        await application.updater.start_polling(drop_pending_updates=True)

        print("RUNNING")

        while True:
            await asyncio.sleep(3600)

    loop.run_until_complete(main())

# ---------------- START BOTH ----------------

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
