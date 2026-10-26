import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

ISM, FAMILIYA, YONALISH, GURUH, TELEFON = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n\n"
        "Ijodkorlar klubiga ro'yxatdan o'tamiz.\n\n"
        "Ismingizni yozing:"
    )
    return ISM

async def ism(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text
    await update.message.reply_text("Familiyangizni yozing:")
    return FAMILIYA

async def familiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["familiya"] = update.message.text
    await update.message.reply_text("Yo'nalishingizni yozing:")
    return YONALISH

async def yonalish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["yonalish"] = update.message.text
    await update.message.reply_text("Guruhingizni yozing:")
    return GURUH

async def guruh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["guruh"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni yozing:")
    return TELEFON

async def telefon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefon"] = update.message.text

    user = update.effective_user
    username = f"@{user.username}" if user.username else "Username yo'q"

    d = context.user_data

    await update.message.reply_text(
        "✅ Ro'yxatdan o'tish yakunlandi!\n\n"
        f"👤 Ism: {d['ism']}\n"
        f"👤 Familiya: {d['familiya']}\n"
        f"🎓 Yo'nalish: {d['yonalish']}\n"
        f"👥 Guruh: {d['guruh']}\n"
        f"📱 Telefon: {d['telefon']}\n"
        f"💬 Telegram: {username}\n\n"
        "Keyingi bosqichda ma'lumotlarni bazaga saqlashni qo'shamiz."
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ro'yxatdan o'tish bekor qilindi.")
    return ConversationHandler.END

def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = Application.builder().token(token).build()

    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism)],
            FAMILIYA: [MessageHandler(filters.TEXT & ~filters.COMMAND, familiya)],
            YONALISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, yonalish)],
            GURUH: [MessageHandler(filters.TEXT & ~filters.COMMAND, guruh)],
            TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conversation)

    print("Ijodkorlar klubi boti ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
