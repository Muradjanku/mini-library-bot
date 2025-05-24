import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

# TO'G'RILANGAN: TOKEN to'g'ridan-to'g'ri yozilgan
TOKEN = "7797937191:AAHJBPfOQVKLB0wzMiVKQoncVeTWvSWmyn0"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_data = {}

def get_language_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("O‘zbek"), KeyboardButton("Русский"))
    return markup

def get_main_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'uz':
        markup.add(KeyboardButton("Umumiy ma'lumot"), KeyboardButton("Yo‘nalishlar"))
        markup.add(KeyboardButton("Qabul shartlari"), KeyboardButton("Tilni o‘zgartirish"))
    else:
        markup.add(KeyboardButton("Общая информация"), KeyboardButton("Направления"))
        markup.add(KeyboardButton("Условия поступления"), KeyboardButton("Сменить язык"))
    return markup

def get_program_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'uz':
        buttons = [
            "Kiberxavfsizlik injiniringi", "Kompyuter injiniringi", "Dasturiy injiniring",
            "Yurisprudensiya", "Menejment", "Iqtisodiyot",
            "Axborot xavfsizligi", "Kiber huquq", "Orqaga"
        ]
    else:
        buttons = [
            "Кибербезопасность", "Компьютерная инженерия", "Программная инженерия",
            "Юриспруденция", "Менеджмент", "Экономика",
            "Информационная безопасность", "Кибер право", "Назад"
        ]
    for btn in buttons:
        markup.add(KeyboardButton(btn))
    return markup

program_info_uz = {
    "Kiberxavfsizlik injiniringi": (
        "🛡️ *Kiberxavfsizlik injiniringi*\n"
        "• Tahdidlarni aniqlash, ularni oldini olish va tizimlarni himoyalash usullari.\n"
        "• Amaliy mashg‘ulotlar xalqaro standartlar asosida.\n"
        "• Ish o‘rinlari: CERT, SOC, IT bo‘limlar."
    ),
    "Kompyuter injiniringi": (
        "💻 *Kompyuter injiniringi*\n"
        "• Tizim arxitekturasi va apparat-dasturiy integratsiya.\n"
        "• Real loyihalar asosida o‘qitiladi."
    ),
    "Dasturiy injiniring": (
        "🧠 *Dasturiy injiniring*\n"
        "• Versiya nazorati, testlash, ishlab chiqish jarayonlari.\n"
        "• Python, Java, Web, AI asosida."
    ),
    "Yurisprudensiya": (
        "⚖️ *Yurisprudensiya*\n"
        "• Xalqaro va shartnomaviy huquq.\n"
        "• Kiberhuquq asoslari bilan."
    ),
    "Menejment": (
        "📊 *Menejment*\n"
        "• Biznes jarayonlari va yetakchilik.\n"
        "• IT kompaniyalarda amaliyot."
    ),
    "Iqtisodiyot": (
        "📈 *Iqtisodiyot*\n"
        "• Raqamli iqtisod, moliya, statistika.\n"
        "• Tahliliy fikrlash topshiriqlari bilan."
    ),
    "Axborot xavfsizligi": (
        "🛡️ *Magistratura: Axborot xavfsizligi*\n"
        "• Penetratsion testlar, forensika, kriptografiya."
    ),
    "Kiber huquq": (
        "⚖️ *Magistratura: Kiber huquq*\n"
        "• Shaxsiy ma’lumotlar, xalqaro axborot huquqi."
    )
}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'lang': None, 'state': 'start'}
    bot.send_message(chat_id, "Tilni tanlang / Выберите язык:", reply_markup=get_language_menu())

@bot.message_handler(func=lambda msg: True)
def main_handler(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_data:
        user_data[chat_id] = {'lang': None, 'state': 'start'}

    lang = user_data[chat_id]['lang']
    state = user_data[chat_id]['state']

    if text in ["O‘zbek", "Tilni o‘zgartirish"]:
        user_data[chat_id] = {'lang': 'uz', 'state': 'main'}
        bot.send_message(chat_id, "Til tanlandi: O‘zbek tili", reply_markup=get_main_menu('uz'))
        return
    elif text in ["Русский", "Сменить язык"]:
        user_data[chat_id] = {'lang': 'ru', 'state': 'main'}
        bot.send_message(chat_id, "Выбран русский язык", reply_markup=get_main_menu('ru'))
        return

    if not lang:
        bot.send_message(chat_id, "Avval tilni tanlang / Сначала выберите язык", reply_markup=get_language_menu())
        return

    if lang == 'uz':
        if text == "Umumiy ma'lumot":
            bot.send_message(chat_id,
                "⚙️ O‘zbekiston Respublikasi Prezidentining 2025-yil 20-yanvardagi PQ–14-sonli qaroriga asosan, Cyber University tashkil etildi.\n"
                "🔗 https://lex.uz/uz/docs/-7332592\n\n"
                "✅ Maqsad: xalqaro raqobatbardosh, innovatsion va amaliy mutaxassislar tayyorlash.\n"
                "📍 Joylashuv: Toshkent viloyati, Nurafshon shahri\n"
                "🌐 Rasmiy sayt: https://csu.uz/uz"
            )
        elif text == "Qabul shartlari":
            bot.send_message(chat_id,
                "🧑‍💻 2025/2026 uchun imkoniyatlar:\n"
                "• 100 ta davlat granti\n"
                "• Sanoat hamkorlari stipendiyalari\n\n"
                "📘 O‘qish:\n"
                "• 1 yil Foundation, 3 yil bakalavriat\n"
                "• To‘liq ingliz tilida\n"
                "• Kredit-modul tizimi\n"
                "• Amaliyot IT kompaniyalarda"
            )
        elif text == "Yo‘nalishlar":
            user_data[chat_id]['state'] = 'programs'
            bot.send_message(chat_id, "Yo‘nalishni tanlang:", reply_markup=get_program_menu(lang))
        elif text in program_info_uz:
            bot.send_message(chat_id, program_info_uz[text], parse_mode='Markdown')
        elif text == "Orqaga":
            user_data[chat_id]['state'] = 'main'
            bot.send_message(chat_id, "Asosiy menyu", reply_markup=get_main_menu(lang))
        else:
            bot.send_message(chat_id, "Iltimos, menyudan tanlang.")
    else:
        bot.send_message(chat_id, "Русский язык — tez orada qo‘shiladi.")

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
