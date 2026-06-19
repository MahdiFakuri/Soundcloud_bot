import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8862830628:AAFvNAbijon5QxxC3sQ0b4a-KHpdFqtv5bQ"

async def handle_message(update, context):
    url = update.message.text

    await update.message.reply_text("در حال دانلود...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    if not os.path.exists(filename):
        for f in os.listdir():
            if f.endswith((".mp3", ".m4a", ".opus", ".webm")):
                filename = f
                break

    await update.message.reply_audio(audio=open(filename, 'rb'))
    os.remove(filename)

    for file in os.listdir():
        if file.endswith(".mp3") or file.endswith(".m4a"):
            await update.message.reply_audio(audio=open(file, 'rb'))
            os.remove(file)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
