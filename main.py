
import os


import spacex_images
import nasa_epic_images
import nasa_apod_images
import telegram_api


from dotenv import load_dotenv


def main():
    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN', default='DEMO_KEY')
    images_dir = os.getenv('IMAGES_DIR', default=os.path.join('', 'images'))
    chat_id = os.environ['TG_CHAT_ID']
    bot_token = os.environ['TG_BOT_TOKEN']
    delay = int(os.getenv('TG_DELAY', default='14400'))
    max_size = int(os.getenv('TG_MAX_SIZE', default='3145728'))
    os.makedirs(images_dir, exist_ok=True)
    nasa_apod_images.load_apod_pictures(images_dir, nasa_token)
    spacex_images.fetch_spacex_launch(images_dir, 'latest')
    nasa_epic_images.load_epic_pictures(images_dir, nasa_token)
    telegram_api.start_bot(bot_token, images_dir, chat_id, delay, max_size)


if __name__ == '__main__':
    main()


