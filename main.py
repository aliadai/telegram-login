import os
import telebot

# طباعة التوكن للتأكد
print("🔍 BOT_TOKEN =", os.getenv("BOT_TOKEN"))

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("❌ لم يتم العثور على BOT_TOKEN! تأكد من إضافته في Railway Variables.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت شغال بنجاح على Railway!")

bot.polling()