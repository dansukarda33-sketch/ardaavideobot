from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot aktif"

def run():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run).start()

import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = '8355170336:AAGH-M77JXOCSMxbwrHmzHFMG5kFaSvYxTA'

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # Sadece link içeren mesajları kontrol et
    if not any(site in url for site in ["twitter.com", "x.com", "facebook.com", "instagram.com"]):
        return

    await update.message.reply_text("Video işleniyor, lütfen bekle...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        os.remove('video.mp4')
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()

