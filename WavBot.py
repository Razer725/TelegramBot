import telebot
import os
import sqlite3
import wave
from urllib.request import urlopen
import soundfile
from pydub import AudioSegment
import io

# data = soundfile.read('t_voice5328001140795639231.ogg')
# soundfile.write('tawda.wav', data, 16000)


sound = AudioSegment.from_ogg(r'C:\Users\Иван\PycharmProjects\TeleBotWavSave\DescenteInfinie.ogg')



if os.path.exists('TeleBotWavSave.db'):
    conn = sqlite3.connect('TeleBotWavSave.db')
else:
    conn = sqlite3.connect('TeleBotWavSave.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE BOT_SAVE
                    (USER_ID, FILE_ID, VOICE, WAV, PHOTO)
                    """)

with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM BOT_SAVE")
    rows = cur.fetchall()
    print(rows)

bot = telebot.TeleBot('1008610085:AAEfDVp8c_xR2-EZ4f5mELCejbMXFS5i5Tc')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


# @bot.message_handler(content_types=['voice'])
# def save_voice(message):
#     bot.send_message(message.chat.id, 'Сохраняю')
#     file_id = message.voice.file_id
#     file = bot.get_file(file_id)
#
#
#     downloaded_file = bot.download_file(file.file_path)
#     user_id = message.from_user.id
#
#     with open(os.getcwd() + '\\' + str(file_id) + '.ogg', 'wb') as file_out:
#         file_out.write(downloaded_file)
#
#
# bot.polling()

