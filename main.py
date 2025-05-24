import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = "7953800384:AAGUF3MW1H_zlT3gTOjvyUBX9bxMvNCO5l4"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Kitoblar bazasi (oddiy ro'yxat sifatida)
books = [
    "Ufq – Cho‘lpon",
    "Mehrobdan chayon – Pirimqul Qodirov",
    "Ikki eshik orasi – O‘tkir Hoshimov",
    "Dunyoning ishlari – O‘tkir Hoshimov",
    "Qorako‘z Majnun – Erkin Vohidov"
]

# Boshlang‘ich menyu
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 Kitob qidirish"), KeyboardButton("ℹ️ Bot haqida"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📓 Istalgan kitobingizni topib beradgan bot!\n\n"
                              "Iltimos, menyudan tanlang:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Bot haqida")
def about(message):
    bot.send_message(message.chat.id, 
        "Bu bot orqali siz O‘zbek adabiyotiga oid kitoblarni tezda topishingiz mumkin.\n"
        "Agar kitob chiqmasa, demak bazamizga qo‘shilmagan!")

@bot.message_handler(func=lambda msg: msg.text == "📚 Kitob qidirish")
def ask_book(message):
    bot.send_message(message.chat.id, "Qidirayotgan kitob nomini kiriting:")

@bot.message_handler(func=lambda msg: True)
def search_book(message):
    text = message.text.lower()
    found = [book for book in books if text in book.lower()]
    
    if found:
        reply = "🔍 Topilgan kitoblar:\n\n" + "\n".join(f"• {b}" for b in found)
    elif text not in ["📚 kitob qidirish", "ℹ️ bot haqida"]:
        reply = "😔 Afsuski, bu kitob bazamizda yo‘q.\n\n" \
                "Bizga taklif qilishingiz mumkin!"

    else:
        return

    bot.send_message(message.chat.id, reply)

# Webhook endpoint
@app.route("/", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://muradjanku.up.railway.app/")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
