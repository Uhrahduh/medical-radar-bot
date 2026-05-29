from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from radar import scan_jobs
from config import TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        f"🧠 Radar activo.\nCHAT ID: {chat_id}"
    )

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Escaneando hospitales..."
    )

    jobs = scan_jobs()

    if not jobs:
        await update.message.reply_text(
            "No se encontraron resultados."
        )
        return

    for job in jobs:
        await update.message.reply_text(job)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))

if __name__ == "__main__":
    app.run_polling()
