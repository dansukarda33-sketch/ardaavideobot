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
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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

# Flask sunucusu (Render'ın botu uyutmaması için)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Flask sunucusu
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"
if __name__ == '__main__':
    # Flask'ı başlat
    port = int(os.environ.get("PORT", 10000))
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()

    # Botu başlat
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    
    print("Bot başlatılıyor...")
    app_bot.run_polling()
