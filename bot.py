import telebot
import yt_dlp
import os
import time

# التوكن الخاص بك
TOKEN = '8643245025:AAE5E-8rS_ldojiNgWv0AaSM7xhYf_xtCI8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا صقر! 👋\nأرسل لي أي رابط فيديو (يوتيوب، تيك توك، إنستغرام) وسأستخرج لك روابط التحميل.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if not url.startswith('http'):
        return

    msg = bot.reply_to(message, "⏳ جاري فحص الرابط بأقصى سرعة...")

    # إعدادات متقدمة لتجاوز الحماية والقيود
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'no_color': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'فيديو بدون عنوان')
            
            # استخراج أفضل رابط تحميل مباشر
            download_url = info.get('url')
            ext = info.get('ext', 'mp4')

            if download_url:
                response_text = f"✅ **تم العثور على الفيديو:**\n{title}\n\n"
                response_text += f"🔗 [اضغط هنا لتحميل الفيديو مباشرة بصيغة {ext}]({download_url})"
                bot.edit_message_text(response_text, msg.chat.id, msg.message_id, parse_mode='Markdown')
            else:
                bot.edit_message_text("❌ لم أتمكن من استخراج رابط مباشر، جرب رابطاً آخر.", msg.chat.id, msg.message_id)

    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text(f"❌ عذراً، هذا الموقع يفرض قيوداً حالياً. جرب رابط يوتيوب أو تيك توك آخر.", msg.chat.id, msg.message_id)

# نظام التشغيل اللانهائي للسحاب
if __name__ == "__main__":
    print("البوت بدأ العمل في السحاب...")
    bot.infinity_polling(timeout=90, long_polling_timeout=30)
