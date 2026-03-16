import telebot
import yt_dlp
import os
import time

TOKEN = '8643245025:AAE5E-8rS_ldojiNgWv0AaSM7xhYf_xtCI8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا صقر! 🦅\nأرسل الرابط وسأحاول تحميله لك بأعلى دقة ممكنة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if not url.startswith('http'): return

    msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو بأعلى جودة متوفرة... فضلاً انتظر.")
    filename = f"video_{message.chat.id}_{int(time.time())}.mp4"

    ydl_opts = {
        # يختار أفضل جودة فيديو + أفضل جودة صوت ويدمجهم في mp4
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': filename,
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # فحص حجم الملف قبل الإرسال (حد تليجرام للبوتات هو 50MB)
        filesize = os.path.getsize(filename) / (1024 * 1024) # تحويل للميجابايت
        
        if filesize > 50:
            bot.edit_message_text(f"⚠️ الفيديو حجمه {filesize:.1f}MB وهو أكبر من حد تليجرام (50MB).\nحاول إرسال مقطع أقصر للحفاظ على الدقة العالية.", msg.chat.id, msg.message_id)
        else:
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"✅ تم التحميل بأعلى دقة متوفرة\n📦 الحجم: {filesize:.1f} MB", supports_streaming=True)
            bot.delete_message(message.chat.id, msg.message_id)
        
        os.remove(filename)

    except Exception as e:
        bot.edit_message_text("❌ حدث خطأ أثناء التحميل. تأكد من الرابط أو حاول لاحقاً.", msg.chat.id, msg.message_id)
        if os.path.exists(filename): os.remove(filename)

if __name__ == "__main__":
    bot.infinity_polling()
