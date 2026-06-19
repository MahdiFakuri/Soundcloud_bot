import os
import re
import requests
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8862830628:AAFvNAbijon5QxxC3sQ0b4a-KHpdFqtv5bQ"


# استخراج لینک واقعی از متن (مشکل اصلی تو حل میشه)
def extract_url(text: str) -> str | None:
    urls = re.findall(r'https?://\S+', text)
    if not urls:
        return None
    return urls[0]


# تبدیل لینک کوتاه SoundCloud به لینک اصلی
def resolve_url(url: str) -> str:
    if "on.soundcloud.com" in url:
        try:
            r = requests.head(url, allow_redirects=True, timeout=10)
            return r.url
        except:
            return url
    return url


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    url = extract_url(text)

    if not url:
        await update.message.reply_text("هیچ لینکی پیدا نشد ❌")
        return

    url = resolve_url(url)

    await update.message.reply_text("در حال دانلود... 🎧")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
        'noplaylist': True
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

        if not filename:
            await update.message.reply_text("دانلود ناموفق بود ❌")
            return

        await update.message.reply_audio(audio=open(filename, 'rb'))
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"خطا ❌\n{str(e)}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
