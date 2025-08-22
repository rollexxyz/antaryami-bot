import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Dummy Flask server to satisfy Render's port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "ANTARYAMI BOT is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Lecture database: 001 to 300 with fixed topic and batch
lecture_data = {
    str(i).zfill(3): {
        "topic": "HISTORY",
        "batch": "G.S CRASH COURSE BY KHAN SIR"
    }
    for i in range(1, 301)
}

# /post command handler
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        lecture_number = context.args[0].zfill(3)
        link = context.args[1]
        data = lecture_data.get(lecture_number)

        if data:
            message = f"""
📚 <b>Batch:</b> {data['batch']}  
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

# Telegram bot runner
def run_bot():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("post", post))
    app.run_polling()

# Start both Flask and Telegram bot
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
