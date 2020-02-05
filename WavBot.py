import telebot
import os

bot = telebot.TeleBot('1008610085:AAEfDVp8c_xR2-EZ4f5mELCejbMXFS5i5Tc')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['voice'])
def save_voice(message):
    bot.send_message(message.chat.id, 'Сохраняю')
    file_id = message.voice.file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    user_id = message.from_user.id
    with open(os.getcwd() + '/' + str(user_id) + '.ogg', 'wb') as file_out:
        file_out.write(downloaded_file)


bot.polling()
