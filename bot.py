import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# ======================
# CONFIG
# ======================
TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# ======================
# TELEGRAM APP
# ======================
application = Application.builder().token(TOKEN).build()

# ======================
# HANDLER
# ======================
async def start(update: Update, context):
    await update.message.reply_text("Bot activo 🚀")

application.add_handler(CommandHandler("start", start))

# ======================
# WEBHOOK ENDPOINT
# ======================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ======================
# HEALTH CHECK
# ======================
@app.route("/")
def home():
    return "Bot running"

# ======================
# SET WEBHOOK (SYNC SAFE)
# ======================
def setup_webhook():
    url = os.getenv("RENDER_EXTERNAL_URL")
    if url:
        webhook_url = f"{url}/webhook"
        application.bot.set_webhook(webhook_url)
        print("Webhook set:", webhook_url)

# ======================
# START
# ======================
if __name__ == "__main__":

    if not TOKEN:
        print("ERROR: BOT_TOKEN missing")
        exit(1)

    setup_webhook()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
