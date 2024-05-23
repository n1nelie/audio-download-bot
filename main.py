import os
import telebot
from telebot import types
import yt_dlp
import re

# Получение токена бота из файла
match os.name:
    case 'nt':
        secrets_path = "secrets\\secret_token.txt"
    case 'posix':
        secrets_path = "secrets/secret_token.txt"

with open(secrets_path, "r", encoding='utf-8') as file:
    TOKEN = file.read().strip()

bot = telebot.TeleBot(TOKEN)

# Регулярное выражение для проверки валидности ссылки на YouTube
youtube_url_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')


# Обрабатываем команду /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Скачать музыку")
    item2 = types.KeyboardButton("Скачать видео")
    item3 = types.KeyboardButton("Voice Message")
    markup.add(item1, item2, item3)

    bot.reply_to(message,
                 "Привет! Это бот позволяющий скачивать музыку, видео или получение звуковой дорожки с видео в качестве аудиосообщения. Для выбора нужной функции воспользуйтесь меню!",
                 reply_markup=markup)


# Обрабатываем входящие сообщения с текстом
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "Скачать музыку":
        bot.reply_to(message, "Отправьте ссылку на видео, чтобы скачать музыку.")
        bot.register_next_step_handler(message, download_audio)
    elif message.text == "Скачать видео":
        bot.reply_to(message, "Отправьте ссылку на видео, чтобы скачать его.")
        bot.register_next_step_handler(message, download_video)
    elif message.text == "Voice Message":
        bot.reply_to(message, "Отправьте ссылку на видео, чтобы отправить голосовое сообщение.")
        bot.register_next_step_handler(message, send_voice_message)
    else:
        bot.reply_to(message, "Извините, могу обработать только ссылки на YouTube")


def download_audio(message):
    url = message.text
    if not youtube_url_regex.match(url):
        bot.reply_to(message, "Неверный формат ссылки. Пожалуйста, отправьте корректную ссылку на YouTube.")
        return
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
        }
        bot.reply_to(message, f"Пытаюсь обработать ссылку: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        chat_id = message.chat.id
        audio_file = open(audio_file_path, 'rb')
        bot.send_audio(chat_id, audio_file)
        audio_file.close()
        os.remove(audio_file_path)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


def download_video(message):
    url = message.text
    if not youtube_url_regex.match(url):
        bot.reply_to(message, "Неверный формат ссылки. Пожалуйста, отправьте корректную ссылку на YouTube.")
        return
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/webm',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'webm',
        }
        bot.reply_to(message, f"Пытаюсь обработать ссылку: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file_path = ydl.prepare_filename(info_dict)

        # Проверка размера файла перед отправкой
        file_size = os.path.getsize(video_file_path)
        if file_size > 50 * 1024 * 1024:  # 50 MB
            bot.reply_to(message, "Произошла ошибка: Размер файла превышает 50 МБ.")
            os.remove(video_file_path)
            return

        chat_id = message.chat.id
        video_file = open(video_file_path, 'rb')
        bot.send_video(chat_id, video_file)
        video_file.close()
        os.remove(video_file_path)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


def send_voice_message(message):
    url = message.text
    if not youtube_url_regex.match(url):
        bot.reply_to(message, "Неверный формат ссылки. Пожалуйста, отправьте корректную ссылку на YouTube.")
        return
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
        }
        bot.reply_to(message, f"Пытаюсь обработать ссылку: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        chat_id = message.chat.id
        audio_file = open(audio_file_path, 'rb')
        bot.send_voice(chat_id, audio_file)
        audio_file.close()
        os.remove(audio_file_path)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


bot.polling()
