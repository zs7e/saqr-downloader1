import telebot
import yt_dlp
import os
import time

TOKEN = '8643245025:AAE5E-8rS_ldojiNgWv0AaSM7xhYf_xtCI8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if not url.startswith('http'): return

    msg = bot.reply_to(message, "🚀 جاري التحميل بأفضل تقنية متاحة...")
    filename = f"video_{message.chat.id}_{int(time.time())}.mp4"

    ydl_opts = {
        'format': 'best', # اختيار أفضل جودة مدمجة لتجنب فشل السيرفر
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
        # محاكاة الدخول من السعودية لتجاوز الحظر الجغرافي
        'source_address': '0.0.0.0', # يمنع بعض أنواع الحظر
        'geo_bypass': True,
        'geo_bypass_country': 'SA',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل بواسطة صقر")
        
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ المواقع تفرض حماية عالية على هذا الرابط حالياً.", msg.chat.id, msg.message_id)
