import os
import yt_dlp
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters


TOKEN = '8355170336:AAFm-ZNziE2JCbwGJTcMDNIuTZJ2OVIyWXQ'

# Flask ile "uykuya dalmama" (keep-alive) mekanizması
app = Flask('')
@app.route('/')
def home():
    return "Bot aktif"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run_flask, daemon=True).start()

# Video indirme fonksiyonu
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # Desteklenen siteler
    supported_sites = ["twitter.com", "x.com", "facebook.com", "instagram.com", "youtube.com", "youtu.be", "tiktok.com"]
    if not any(site in url for site in supported_sites):
        return

    status_msg = await update.message.reply_text("Video işleniyor, lütfen bekle...")
    
    # yt-dlp seçenekleri
        ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
        'socket_timeout': 30,
        'retries': 5,
    }

    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Dosya mevcut mu kontrol et
        if os.path.exists('video.mp4'):
            await update.message.reply_video(video=open('video.mp4', 'rb'))
            os.remove('video.mp4')
            await status_msg.delete()
        else:
            await status_msg.edit_text("Video indirilemedi, dosya bulunamadı.")
            
    except Exception as e:
        await status_msg.edit_text(f"Hata oluştu: {str(e)[:100]}")
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

if __name__ == '__main__':
    # Bot kurulumu
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    
    print("Bot başlatılıyor...")
    app_bot.run_polling()
