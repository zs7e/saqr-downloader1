import telebot
import yt_dlp
import os
import time

# التوكن الخاص بك
TOKEN = '8643245025:AAE5E-8rS_ldojiNgWv0AaSM7xhYf_xtCI8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا صقر! 👋\nأرسل لي رابط فيديو (يوتيوب، تيك توك، إنستقرام) وسأرسله لك كملف فيديو مباشرة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if not url.startswith('http'):
        return

    # رسالة تظهر للمستخدم أثناء العمل
    msg = bot.reply_to(message, "⏳ جاري التحميل ومعالجة الفيديو... فضلاً انتظر ثواني.")

    # اسم ملف مؤقت للفيديو لضمان عدم التداخل
    filename = f"video_{message.chat.id}_{int(time.time())}.mp4"

    # إعدادات التحميل (أفضل جودة mp4 لا تتجاوز حجم معين)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # عملية التحميل من الرابط إلى سيرفر Render
            ydl.download([url])
            
        # إرسال ملف الفيديو الفعلي للمستخدم
        with open(filename, 'rb') as video:
            bot.send_video(
                message.chat.id, 
                video, 
                caption="✅ تم التحميل بواسطة بوت صقر",
                supports_streaming=True # يتيح للمستخدم مشاهدة الفيديو أثناء التحميل
            )
        
        # حذف الملف من السيرفر فوراً بعد الإرسال
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text("❌ عذراً، تعذر تحميل الفيديو. قد يكون الرابط غير مدعوم أو الحجم كبيراً جداً.", msg.chat.id, msg.message_id)
        # التأكد من حذف الملف في حال حدوث خطأ
        if os.path.exists(filename):
            os.remove(filename)

# تشغيل البوت بشكل مستمر
if __name__ == "__main__":
    print("البوت بدأ العمل بنظام الإرسال المباشر...")
    bot.infinity_polling()
