import telebot
import requests

# 👇 PON AQUÍ TU TOKEN DE @BotFather
TOKEN = "8919850373:AAFNlGF93_QhjuCLaqqwDWMnwL2dQoJmj7s"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def inicio(mensaje):
    bot.reply_to(mensaje, "👋 ¡Hola! Usa /numero para obtener un número virtual gratis 🇺🇸🇪🇸🇲🇽\n⚠️ Son compartidos y temporales, no para cuentas bancarias ni personales.")

@bot.message_handler(commands=['numero'])
def dar_numero(mensaje):
    try:
        url = "https://otp-api.shelex.dev/api/list/USA"
        r = requests.get(url)
        data = r.json()

        if not data or len(data) == 0:
            bot.reply_to(mensaje, "❌ No hay números disponibles ahora, intenta más tarde.")
            return

        num = data[0]
        texto = f"📞 Tu número: +1{num}\n📩 Para ver SMS: /sms {num}"
        bot.reply_to(mensaje, texto)

    except Exception as e:
        bot.reply_to(mensaje, "⚠️ Error al obtener número, intenta luego.")

@bot.message_handler(commands=['sms'])
def ver_sms(mensaje):
    try:
        partes = mensaje.text.split()
        if len(partes) < 2:
            bot.reply_to(mensaje, "❗ Escribe: /sms 1234567890")
            return

        num = partes[1]
        url = f"https://otp-api.shelex.dev/api/USA/{num}"
        r = requests.get(url)
        sms = r.json()

        if not sms or len(sms) == 0:
            bot.reply_to(mensaje, "📭 Aún no hay mensajes, espera 1-2 min y prueba otra vez.")
            return

        texto = "📨 Mensajes recibidos:\n"
        for m in sms[:5]:
            texto += f"🕒 {m['time']} | De: {m['from']}\n📄 {m['text']}\n---\n"

        bot.reply_to(mensaje, texto)

    except Exception as e:
        bot.reply_to(mensaje, "⚠️ Error al leer mensajes.")

print("✅ Bot funcionando...")
bot.polling()
                          
