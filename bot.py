import telebot
import yt_dlp
import os
import time

# تأكد من وضع التوكن الصحيح هنا
TOKEN = '8643245025:AAE5E-8rS_ldojiNgWv0AaSM7xhYf_xtCI8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "هلا صقر! 🦅\nأرسل الرابط وابشر بأعلى دقة متوفرة (يوتيوب، تيك توك، إنستقرام).")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if not url.startswith('http'): return

    msg = bot.reply_to(message, "⏳ جاري التحميل بأقصى دقة.. قد يستغرق اليوتيوب وقتاً أطول قليلاً.")
    filename = f"video_{message.chat.id}_{int(time.time())}.mp4"

    ydl_opts = {
        # اختيار أعلى دقة فيديو وأعلى دقة صوت ودمجهم
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': filename,
        'merge_output_format': 'mp4',
        'quiet': True,
        # إضافة هوية متصفح حقيقي لتجنب حظر يوتيوب وإنستقرام
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        filesize = os.path.getsize(filename) / (1024 * 1024)
        
        # تليجرام يسمح برفع 50 ميجابايت كحد أقصى للبوتات العادية
        if filesize > 50:
            bot.edit_message_text(f"⚠️ الفيديو حجمه {filesize:.1f}MB (أكبر من حد 50MB).\nتم التحميل بالدقة العالية لكن تليجرام يرفض إرساله.\nجرب فيديو أقصر قليلاً بنفس الدقة.", msg.chat.id, msg.message_id)
        else:
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"✅ تم التحميل بأعلى دقة متوفرة\n📦 الحجم: {filesize:.1f} MB", timeout=120, supports_streaming=True)
            bot.delete_message(message.chat.id, msg.message_id)
        
        if os.path.exists(filename): os.remove(filename)

    except Exception as e:
        # إذا فشل بسبب الحظر أو الحقوق تظهر هذه الرسالة
        bot.edit_message_text("❌ تعذر التحميل. قد يكون الفيديو محمياً أو يتطلب تسجيل دخول.", msg.chat.id, msg.message_id)
        if os.path.exists(filename): os.remove(filename)

if __name__ == "__main__":
    bot.infinity_polling()
