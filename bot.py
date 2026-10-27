from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
import os

ISM_FAMILIYA, YONALISH, GURUH, TELEFON = range(4)

YONALISHLAR = [
    "Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar",
    "Moliya va moliyaviy texnologiyalar",
    "Islomiy moliya",
    "Bank ishi",
    "Buxgalteriya hisobi",
    "Soliqlar va soliqqa tortish",
    "Davlat auditi",
    "Statistika",
    "Menejment",
    "Biznesni boshqarish",
    "Marketing",
    "Inson resurslarini boshqarish",
    "Savdo ishi",
    "Logistika",
    "Turizm va mehmondo‘stlik",
    "Axborot xavfsizligi",
    "Axborot tizimlari va texnologiyalari",
    "Sun’iy intellekt"
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "🎨 Ijodkorlar klubiga xush kelibsiz!\n\n"
        "Ro‘yxatdan o‘tish uchun ma’lumotlaringizni kiriting.\n\n"
        "👤 Ism va familiyangizni yozing:\n"
        "Masalan: Afruzbek Xushboqov"
    )

    return ISM_FAMILIYA


async def ism_familiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism_familiya"] = update.message.text

    keyboard = []

    # Har bir yo‘nalishni alohida tugma qilib chiqaramiz
    for yonalish in YONALISHLAR:
        keyboard.append([yonalish])

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "🎓 Yo‘nalishingizni tanlang:",
        reply_markup=reply_markup
    )

    return YONALISH


async def yonalish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tanlangan = update.message.text

    if tanlangan not in YONALISHLAR:
        await update.message.reply_text(
            "❗ Iltimos, quyidagi tugmalardan birini tanlang."
        )
        return YONALISH

    context.user_data["yonalish"] = tanlangan

    await update.message.reply_text(
        "👥 Guruhingizni yozing:\n\n"
        "Masalan: MG-81/25",
        reply_markup={"remove_keyboard": True}
    )

    return GURUH


async def guruh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["guruh"] = update.message.text

    keyboard = [[
        KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
    ]]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "📞 Telefon raqamingizni yuboring:\n\n"
        "Quyidagi tugmani bosishingiz mumkin.",
        reply_markup=reply_markup
    )

    return TELEFON


async def telefon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tugma orqali yuborilgan telefon
    if update.message.contact:
        telefon_raqam = update.message.contact.phone_number
    else:
        telefon_raqam = update.message.text

    context.user_data["telefon"] = telefon_raqam

    user = update.effective_user

    if user.username:
        username = "@" + user.username
    else:
        username = "Username yo‘q"

    d = context.user_data

    await update.message.reply_text(
        "✅ RO‘YXATDAN O‘TISH YAKUNLANDI!\n\n"
        f"👤 Ism va familiya: {d['ism_familiya']}\n"
        f"🎓 Yo‘nalish: {d['yonalish']}\n"
        f"👥 Guruh: {d['guruh']}\n"
        f"📞 Telefon: {d['telefon']}\n"
        f"💬 Telegram: {username}\n\n"
        "🎨 Ijodkorlar klubiga xush kelibsiz!"
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Ro‘yxatdan o‘tish bekor qilindi."
    )

    return ConversationHandler.END


# Token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN topilmadi! "
        "Replit Secrets orqali tokenni qo‘shing."
    )


app = Application.builder().token(TOKEN).build()


conversation = ConversationHandler(
    entry_points=[
        CommandHandler("start", start)
    ],

    states={
        ISM_FAMILIYA: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                ism_familiya
            )
        ],

        YONALISH: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                yonalish
            )
        ],

        GURUH: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                guruh
            )
        ],

        TELEFON: [
            MessageHandler(
                filters.CONTACT,
                telefon
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                telefon
            )
        ]
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)


app.add_handler(conversation)

print("✅ Ijodkorlar klubi boti ishga tushdi!")

app.run_polling()
