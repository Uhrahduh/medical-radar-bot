from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN

print("BOT START")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OK FUNCIONA")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
