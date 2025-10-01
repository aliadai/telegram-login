from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BOT_TOKEN = "7721018260:AAF3Agdm5HTp7d6ibMTPURniPMdwQi2BBRQ"  
ADMIN_ID = 7182427468      # آيديك إنت

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth", methods=["POST"])
def auth():
    data = request.form.to_dict()
    user_id = data.get("id")
    first_name = data.get("first_name")

    text = f"💌 حرب يريدك بحياته ويرتبط بيك يا {first_name}!\nشنو رأيك؟"

    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ موافق", "callback_data": f"accept_{user_id}"}],
            [{"text": "❌ رافض", "callback_data": f"reject_{user_id}"}]
        ]
    }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": user_id, "text": text, "reply_markup": str(keyboard)}
    requests.post(url, data=payload)

    return "تم الإرسال ✅"


# Webhook لمعالجة ضغط الأزرار
@app.route("/callback", methods=["POST"])
def callback():
    data = request.json

    if "callback_query" in data:
        query = data["callback_query"]
        from_id = query["from"]["id"]
        action = query["data"]

        # نفرز الـ action
        if action.startswith("accept_"):
            user = action.split("_")[1]
            msg = f"✅ المستخدم {from_id} وافق على الطلب (ID: {user})"
        elif action.startswith("reject_"):
            user = action.split("_")[1]
            msg = f"❌ المستخدم {from_id} رفض الطلب (ID: {user})"
        else:
            msg = "⚠️ حدث خطأ بالمعالجة."

        # نرسل النتيجة لإلك
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": ADMIN_ID, "text": msg}
        )

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)