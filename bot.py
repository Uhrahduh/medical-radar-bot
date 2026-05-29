from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN
from radar import scan_jobs
import asyncio

print("🧠 RADAR MÉDICO INICIADO")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Radar activo en Ruhrgebiet")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = scan_jobs()

    if not jobs:
        await update.message.reply_text("🔎 No se detectaron vacantes nuevas")
        return

    for job in jobs:
        await update.message.reply_text(job)

async def auto_scan(app):
    while True:
        jobs = scan_jobs()

        for job in jobs:
            try:
                await app.bot.send_message(chat_id=app.chat_id, text=job)
            except:
                pass

        await asyncio.sleep(300)  # 5 minutos


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    print("BOT RUNNING")

    app.run_polling()


if __name__ == "__main__":
    main()
