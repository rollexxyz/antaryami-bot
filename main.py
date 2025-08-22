from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Lecture database
lecture_data = {
    "01": {"topic": "Ancient History", "batch": "GS Crash Course by Khan Sir"},
    "02": {"topic": "Medieval History", "batch": "GS Crash Course by Khan Sir"},
    "03": {"topic": "Modern History", "batch": "GS Crash Course by Khan Sir"},
    "04": {"topic": "World History", "batch": "GS Crash Course by Khan Sir"},
    "05": {"topic": "History", "batch": "GS Crash Course by Khan Sir"},
    # Add more lectures as needed
}

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        lecture_number = context.args[0]
        link = context.args[1]
        data = lecture_data.get(lecture_number)

        if data:
            message = f"""
📚 <b>{data['batch']}</b>
🎓 <b>Topic:</b> {data['topic']}
🎥 <b>Lecture {lecture_number}</b>
🔗 <b>Watch Now:</b> <a href="{link}">{link}</a>

🧠 <b>Powered by ANTARYAMI BOT 🔥</b>
"""
            await update.message.reply_html(message)
        else:
            await update.message.reply_text("❌ Lecture number not found in database.")
    except:
        await update.message.reply_text("⚠️ Format error. Use: /post <lecture_number> <youtube_link>")

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("post", post))
    app.run_polling()

if __name__ == "__main__":
    main()