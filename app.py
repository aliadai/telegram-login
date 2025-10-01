from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BOT_TOKEN = "توكن_البوت"
# ما تحتاج ADMIN_ID هنا، لأن الرسالة راح تنرسل للشخص المسجل دخول

@app.route("/")
def index():
    return render_template("index.html")  # بيه زر تسجيل الدخول

@app.route("/auth", methods=["POST"])
def auth():
    data = request.form.to_dict()
    user_id = data.get("id")   # يجي من Telegram login widget
    first_name = data.get("first_name")

    text = f"💌 حرب يريدك بحياته ويرتبط بيك يا {first_name}!\nشنو رأيك؟"

    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ موافق", "callback_data": "accept"}],
            [{"text": "❌ رافض", "callback_data": "reject"}]
        ]
    }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": user_id, "text": text, "reply_markup": str(keyboard)}
    requests.post(url, data=payload)

    return "تم الإرسال ✅"