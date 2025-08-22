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
    return "ANTARYAMI BOT is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ✅ Auto-generated lecture database (01–200)
lecture_data = {
    str(i).zfill(2): {
        "topic": f"GS Lecture {str(i).zfill(2)}",
        "batch": "GS Crash Course by Khan Sir"
    }
    for i in range(1, 201)
}

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        lecture_number = context.args[0].zfill(2)
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
    except Exception as e:
        logging.error(f"Error in /post command: {e}")
        await update.message.reply_text("⚠️ Format error. Use: /post <lecture_number> <youtube_link>")

def run_bot():
    try:
        token = os.getenv("BOT_TOKEN")
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("post", post))
        app.run_polling()
    except Exception as e:
        logging.error(f"Bot failed to start: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
