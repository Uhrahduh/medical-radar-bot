from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN
from radar import scan_jobs
import asyncio

print("BOT INICIANDO...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Radar médico activo")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Escaneando...")

    jobs = scan_jobs()

    if not jobs:
        await update.message.reply_text("No resultados")
        return

    for job in jobs:
        await update.message.reply_text(job)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    print("BOT CORRIENDO")

    app.run_polling()

if __name__ == "__main__":
    main()
