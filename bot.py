import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
# HANDLERS
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo en webhook 🚀")

application.add_handler(CommandHandler("start", start))

# ======================
# WEBHOOK ENDPOINT
# ======================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ======================
# HOME (Render health check)
# ======================
@app.route("/")
def home():
    return "Bot running"

# ======================
# START WEBHOOK ON BOOT
# ======================
def set_webhook():
    url = os.getenv("RENDER_EXTERNAL_URL")  # Render lo provee automáticamente
    if url:
        webhook_url = f"{url}/webhook"
        application.bot.set_webhook(webhook_url)
        print(f"Webhook set to: {webhook_url}")

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: BOT_TOKEN no configurado")
        exit(1)

    set_webhook()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
