import os
import re
import yt_dlp
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8862830628:AAFvNAbijon5QxxC3sQ0b4a-KHpdFqtv5bQ"


def extract_url(text):
    urls = re.findall(r'https?://\S+', text)
    return urls[0] if urls else None


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    url = extract_url(text)

    if not url:
        await update.message.reply_text("لینک پیدا نشد ❌")
        return

    await update.message.reply_text("در حال دانلود... 🎧")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        title = info.get("title", "audio")
        video_id = info.get("id")

        # پیدا کردن فایل
        file_path = None
        for f in os.listdir():
            if f.startswith("audio"):
                file_path = f
                break

        if not file_path:
            await update.message.reply_text("دانلود ناموفق ❌")
            return

        # کاور یوتیوب
        thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        await update.message.reply_audio(
            audio=open(file_path, "rb"),
            title=title,
            caption="🎧 Done"
        )

        # ارسال کاور جدا
        await update.message.reply_photo(photo=thumb_url)

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"خطا ❌\n{e}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot running...")
app.run_polling()
