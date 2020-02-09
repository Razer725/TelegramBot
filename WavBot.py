import telebot
import os
import sqlite3
import subprocess
import cv2

"""The bot automatically saves all audio messages from groups to the database.
Converts all audio messages to wav format with a sampling frequency of 16kHz. Files are placed in a folder: Voice
Detects the presence of a face in the photos being sent, saves only where it is"""

TELEGRAM_API_TOKEN = '1008610085:AAEfDVp8c_xR2-EZ4f5mELCejbMXFS5i5Tc'
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


def convert_to_wav(path, file_directory, fileid, user_id):
    """
    File decoded from .ogg to .wav with sample rate 16 kHz
    Output file name format: audio_message_fileid
    """
    conn = sqlite3.connect('TeleBotWavSave.db')  # connect to db
    cursor = conn.cursor()

    # Request to the command line for access to ffmpeg
    converted_path_to_file = '{}audio_message_{}'.format(file_directory, fileid) + '.wav'
    converted_file_id = 'audio_message_{}'.format(fileid) + '.wav'
    command = [r'Voice\ffmpeg.exe', '-i', path + '.ogg', '-ar', '16000', converted_path_to_file]
    subprocess.run(command)

    # Insert in database
    cursor.execute("INSERT INTO BOT_SAVED_FILES (FILE_ID, USER_ID, FILE_TYPE, PATH_TO_FILE) VALUES (?,?,?,?)",
                   (converted_file_id, user_id, 'wav', converted_path_to_file))
    conn.commit()
    conn.close()
    return


if os.path.exists('TeleBotWavSave.db'):
    pass
else:
    conn = sqlite3.connect('TeleBotWavSave.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE BOT_SAVED_FILES
                    (FILE_ID, USER_ID, FILE_TYPE, PATH_TO_FILE)
                    """)
    conn.commit()
    conn.close()

# conn = sqlite3.connect('TeleBotWavSave.db')
# with conn:
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM BOT_SAVED_FILES")
#     rows = cur.fetchall()
#     print(rows, 'database')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """The bot automatically saves all audio messages from groups to the database.
Converts all audio messages to wav format with a sampling frequency of 16kHz. Files are placed in a folder: Voice
Detects the presence of a face in the photos being sent, saves only where it is""")


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    if message.chat.type == 'group':
        conn = sqlite3.connect('TeleBotWavSave.db')  # connect to db
        cursor = conn.cursor()

        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_id = message.from_user.id

        file_directory = os.getcwd() + '\\Voice\\'
        path = file_directory + str(file_id)
        path_to_file = path + '.ogg'

        # Saved file in TeleBotWavSave\Voice
        with open(path_to_file, 'wb') as file_out:
            file_out.write(downloaded_file)

        cursor.execute("INSERT INTO BOT_SAVED_FILES (FILE_ID, USER_ID, FILE_TYPE, PATH_TO_FILE) VALUES (?,?,?,?)",
                       (file_id, user_id, 'ogg', path_to_file))
        conn.commit()
        conn.close()

        convert_to_wav(path, file_directory, str(file_id), user_id)


@bot.message_handler(content_types=['photo'])
def photo_processing(message):
    """
    Bot saves only photos with faces
    """
    file_id = message.photo[len(message.photo) - 1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    user_id = message.from_user.id

    file_directory = os.getcwd() + '\\Photo\\'
    path = file_directory + str(file_id)
    path_to_file = path + '.jpg'

    # Saved file in TeleBotWavSave\Photo
    with open(path_to_file, 'wb') as file_out:
        file_out.write(downloaded_file)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Read the input image
    img = cv2.imread('Photo\\' + str(file_id) + '.jpg')
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:  # If face found
        # Connect to db
        conn = sqlite3.connect('TeleBotWavSave.db')  # connect to db
        cursor = conn.cursor()
        # Insert in database
        cursor.execute("INSERT INTO BOT_SAVED_FILES (FILE_ID, USER_ID, FILE_TYPE, PATH_TO_FILE) VALUES (?,?,?,?)",
                       (file_id, user_id, 'jpg', path_to_file))
        conn.commit()
        conn.close()
    else:
        os.remove(path_to_file)

    # # Draw rectangle around the faces
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # # Display the output
    # cv2.imshow('img', img)
    # cv2.waitKey()


bot.polling()
