from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
from threading import Thread
import os

# Data prediksi
prediksi = {
    17: "BESAR🔥", 21: "BESAR🔥", 24: "KECIL🥶", 25: "KECIL🥶",
    26: "BESAR🔥", 27: "KECIL🥶", 28: "BESAR🔥", 29: "KECIL🥶",
    30: "KECIL🥶", 31: "KECIL🥶", 32: "BESAR🔥", 33: "KECIL🥶",
    34: "BESAR🔥", 35: "KECIL🥶", 36: "BESAR🔥", 37: "KECIL🥶",
    38: "BESAR🔥", 39: "KECIL🥶", 40: "KECIL🥶", 41: "KECIL🥶",
    42: "KECIL🥶", 45: "KECIL🥶"
}

# Tombol start
start_message = """
🎲 *BOT PREDIKSI DADU* 🎲

Silakan ketik angka dadu (misalnya: 28), dan bot akan memprediksi hasilnya berdasarkan data 🔥🥶

Contoh:
`28`
"""

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_message, parse_mode="Markdown")

# Handle angka
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.isdigit():
        angka = int(text)
        if angka in prediksi:
            hasil = prediksi[angka]
            await update.message.reply_text(
                f"""
📥 Angka Dadu: *{angka}*

📊 PRED NEXT:
━━━━━━━━━━━━━━━━━━
✨ *{hasil}*
━━━━━━━━━━━━━━━━━━
📌 _note: jika angka kembar dibalik ya_
                """,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("⚠️ Angka itu belum ada di daftar prediksi, bro!")
    else:
        await update.message.reply_text("❌ Cuma terima angka doang ya bro. Coba ketik contoh: `28`")

# Web server buat uptime
web_app = Flask(__name__)

@web_app.route('/')
def index():
    return "Bot Aktif 🔥"

def run_web():
    web_app.run(host='0.0.0.0', port=8080)

# Bot jalan
async def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ Token belum diset di environment!")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

# Start semua
if __name__ == "__main__":
    from asyncio import run
    Thread(target=run_web).start()
    run(main())