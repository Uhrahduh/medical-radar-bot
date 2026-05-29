from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN
from radar import scan_jobs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Radar activo")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = scan_jobs()

    if not jobs:
        await update.message.reply_text("No resultados")
        return

    for j in jobs:
        await update.message.reply_text(j)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    print("BOT INICIADO")

    app.run_polling()
