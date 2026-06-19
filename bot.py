import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8862830628:AAFvNAbijon5QxxC3sQ0b4a-KHpdFqtv5bQ"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("در حال دانلود... 🎧")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        filename = None

        # پیدا کردن فایل واقعی
        for f in os.listdir():
            if f.startswith("audio") and f.endswith((".mp3", ".m4a", ".opus", ".webm")):
                filename = f
                break

        if filename is None:
            await update.message.reply_text("فایل دانلود نشد ❌ (لینک شاید محدود باشه)")
            return

        await update.message.reply_audio(audio=open(filename, 'rb'))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"خطا در دانلود ❌\n{str(e)}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
