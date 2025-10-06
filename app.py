from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# التوكن من متغير البيئة (حتى ما تكتبه علنيًا)
TOKEN = os.getenv("BOT_TOKEN")

# حالة تفعيل الزر
button_enabled = True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    if button_enabled:
        keyboard = [[InlineKeyboardButton("زر شفاف ✨", url="https://t.me/yourusername")]]
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.message.reply_text("👋 أهلاً! أرسل أي رسالة وسأضيف لها زر شفاف تلقائيًا.", reply_markup=reply_markup)

async def auto_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global button_enabled
    message = update.message
    if not message:
        return

    keyboard = []
    if button_enabled:
        keyboard = [[InlineKeyboardButton("زر شفاف ✨", url="https://t.me/yourusername")]]
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    await message.reply_text(
        f"📩 {message.text}\n\n✅ تمت إضافة الزر تلقائيًا" if button_enabled else f"📩 {message.text}",
        reply_markup=reply_markup
    )

async def toggle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global button_enabled
    if not context.args:
        await update.message.reply_text("استخدم: /toggle on أو /toggle off")
        return

    arg = context.args[0].lower()
    if arg == "on":
        button_enabled = True
        await update.message.reply_text("✅ تم تفعيل الزر التلقائي.")
    elif arg == "off":
        button_enabled = False
        await update.message.reply_text("❌ تم تعطيل الزر التلقائي.")
    else:
        await update.message.reply_text("استخدم: /toggle on أو /toggle off فقط.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("toggle", toggle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_edit))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()