import random
import time
import os
import telegram
import logging

from dotenv import load_dotenv


def get_files(path, max_size):
    result = []
    for item in os.listdir(path):
        file_path = os.path.join(path, item)
        size = os.path.getsize(file_path)
        if size <= max_size:
            result.append(file_path)
    return result


def send_file(bot, chat_id, file_name):
    with open(file_name, 'rb') as opened_file:
        bot.send_document(chat_id=chat_id, document=opened_file)


def start_bot(
    bot_token,
    images_dir,
    chat_id,
    delay,
    max_size
):
    logging.basicConfig(level=logging.ERROR, filename='telegram_log.txt')
    logger = logging.getLogger('telegram_log')
    bot = telegram.Bot(token=bot_token)
    while True:
        files = get_files(images_dir, max_size)
        random.shuffle(files)
        for file in files:
            try:
                send_file(bot, chat_id, file)
            except telegram.error.NetworkError:
                logger.error('Network error')
                time.sleep(60)
                continue
            time.sleep(delay)


def main():
    load_dotenv()
    images_dir = os.getenv('IMAGES_DIR', default=os.path.join('', 'images'))
    os.makedirs(images_dir, exist_ok=True)
    chat_id = os.environ['TG_CHAT_ID']
    bot_token = os.environ['TG_BOT_TOKEN']
    max_size = int(os.getenv('TG_MAX_SIZE', default='3145728'))
    delay = int(os.getenv('TG_DELAY', default='14400'))
    start_bot(bot_token, images_dir, chat_id, delay, max_size)


if __name__ == '__main__':
    main()
