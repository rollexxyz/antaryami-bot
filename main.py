import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import logging

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Dummy Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ ANTARYAMI BOT is running and ready to serve aspirants!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))  # Render sets this automatically
    app.run(host='0.0.0.0', port=port)

# ✅ Subject-wise lecture database
subjects = {
    "gs": {
        "batch": "GS Crash Course by Khan Sir",
        "prefix": "GS Lecture"
    },
    "history": {
        "batch": "History Sprint by Khan Sir",
        "prefix": "History Lecture"
    },
    "polity": {
        "batch": "Polity Power Series",
        "prefix": "Polity Lecture"
    }
}

lecture_data = {
    subject: {
        str(i).zfill(2): {
            "topic": f"{meta['prefix']} {str(i).zfill(2)}",
            "batch": meta["batch"]
        }
        for i in range(1, 201)
    }
    for subject, meta in subjects.items()
}

# ✅ Telegram command handler
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        subject = context.args[0].lower()
        lecture_number = context.args[1].zfill(2)
        link = context.args[2]

        data = lecture_data.get(subject, {}).get(lecture_number)

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
            await update.message.reply_text("❌ Lecture not found for this subject.")
    except Exception as e:
        logging.error(f"Error in /post command: {e}")
        await update.message.reply_text("⚠️ Format error. Use: /post <subject> <lecture_number> <youtube_link>")

# ✅ Bot runner
def run_bot():
    try:
        token = os.getenv("BOT_TOKEN")
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("post", post))
        app.run_polling()
    except Exception as e:
        logging.error(f"Bot failed to start: {e}")

# ✅ Start both Flask and Bot
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
