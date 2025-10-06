# app.py
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN not set")
    exit(1)

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
button_enabled = True

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.reply_to(message, "👋 أهلاً! أرسل أي نص وسأعيد إرساله مع زر شفاف.\nاستخدم /toggle on أو /toggle off")

@bot.message_handler(commands=['toggle'])
def cmd_toggle(message):
    global button_enabled
    parts = message.text.split()
    if len(parts) > 1 and parts[1].lower() in ("on","off"):
        button_enabled = (parts[1].lower() == "on")
        bot.reply_to(message, f"الحالة الآن: {'✅ مفعل' if button_enabled else '❌ معطل'}")
    else:
        bot.reply_to(message, "استخدم: /toggle on أو /toggle off")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    global button_enabled
    # لا نحاول تعديل رسالة المستخدم (هذا غير مسموح للبوت)
    # نرسل رسالة جديدة تحتوي النص + زر شفاف
    if not button_enabled:
        return

    # زر "شفاف" — نستخدم حرف فراغ من نوع braille blank (U+2800) ليكون شبه شفاف
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="\u2800", url="https://t.me/yourusername"))  # عدل URL هنا

    try:
        bot.send_message(message.chat.id, f"✨ تم إعادة إرسال رسالتك:\n{message.text}", reply_markup=kb)
    except Exception as e:
        print("Send error:", e)

if __name__ == "__main__":
    print("Bot polling started...")
    bot.infinity_polling(timeout=20, long_polling_timeout = 5)