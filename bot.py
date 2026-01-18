from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

keyboard = [
    ["🏨 About hotel", "🚕 Transfer"],
    ["🌴 Tours", "📞 Contact"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

SYSTEM_PROMPT = """
You are an AI hotel assistant in Pattaya, Thailand.
You help hotel guests with:
- hotel information
- breakfast time
- Wi-Fi
- transfer
- tours
Answer politely, shortly and clearly.
If question is not about hotel — reply that you help only with hotel services.
Reply in the same language as the guest.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to our hotel 🇹🇭\n"
        "I am your AI assistant.\n"
        "Ask me any question 👇",
        reply_markup=markup
    )

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

app.run_polling()
