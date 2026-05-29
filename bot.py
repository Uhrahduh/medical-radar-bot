import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ======================
# FLASK (Render Web Service)
# ======================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

# ======================
# TELEGRAM BOT
# ======================

TOKEN = os.getenv("BOT_TOKEN")  # IMPORTANTE: usa este nombre exacto en Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo correctamente 🚀")

def run_bot():
    if not TOKEN:
        print("ERROR: BOT_TOKEN no está definido en variables de entorno")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    print("BOT START")
    application.run_polling(drop_pending_updates=True)

# ======================
# MAIN
# ======================
if __name__ == "__main__":

    # iniciar bot en thread separado
    t = threading.Thread(target=run_bot)
    t.start()

    # iniciar flask (IMPORTANTE para Render)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
