import telebot
import requests

# 👇 PON AQUÍ TU TOKEN DE @BotFather
TOKEN = "TU_CODIGO_AQUI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def inicio(mensaje):
    bot.reply_to(mensaje, "👋 ¡Hola! Usa /numero para obtener un número virtual gratis 🇺🇸🇪🇸🇲🇽\n⚠️ Son compartidos y temporales, no para cuentas importantes.")

@bot.message_handler(commands=['numero'])
def dar_numero(mensaje):
    try:
        # 🔴 API NUEVA Y FUNCIONANDO
        url = "https://smsreceivefree.com/api/country/usa"
        r = requests.get(url, timeout=10)
        data = r.json()

        if not data or len(data) == 0:
            bot.reply_to(mensaje, "❌ No hay números ahora, intenta en 5 min.")
            return

        num = data[0]['number']
        id_num = data[0]['id']
        texto = f"📞 Tu número: +1{num}\n📩 Para ver SMS: /sms {id_num}"
        bot.reply_to(mensaje, texto)

    except Exception as e:
        bot.reply_to(mensaje, "⚠️ Error al obtener número, prueba otra vez.")

@bot.message_handler(commands=['sms'])
def ver_sms(mensaje):
    try:
        partes = mensaje.text.split()
        if len(partes) < 2:
            bot.reply_to(mensaje, "❗ Escribe: /sms ID_DEL_NUMERO")
            return

        id_num = partes[1]
        url = f"https://smsreceivefree.com/api/sms/{id_num}"
        r = requests.get(url, timeout=10)
        sms = r.json()

        if not sms or len(sms) == 0:
            bot.reply_to(mensaje, "📭 Aún no hay mensajes, espera 1-2 min.")
            return

        texto = "📨 Mensajes:\n"
        for m in sms[:5]:
            texto += f"🕒 {m['time']} | De: {m['from']}\n📄 {m['text']}\n---\n"

        bot.reply_to(mensaje, texto)

    except Exception as e:
        bot.reply_to(mensaje, "⚠️ Error al leer mensajes.")

print("✅ Bot funcionando...")
bot.polling()
