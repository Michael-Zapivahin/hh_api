
import url_processing
import requests
import datetime
import os
import uuid
import argparse


from urllib.parse import urlparse
from dotenv import load_dotenv


def load_apod_pictures(image_dir, nasa_token, apod_day=None):
    url = 'https://api.nasa.gov/planetary/apod'
    if apod_day is None:
        apod_day = datetime.datetime.now().strftime('%Y-%m-%d')
    payload = {
        'api_key': nasa_token,
        'date': apod_day
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    links = response.json()
    for link in links:
        if not(link == 'media_type' and links[link] == 'image'):
            continue
        url = links['url']
        parsed_url = urlparse(url)
        file_type = url_processing.get_file_type(url)
        if parsed_url.netloc and file_type:
            filename = f'{os.path.join(image_dir, f"apod_{uuid.uuid4()}")}.{file_type}'
            url_processing.download_image(url, filename)


def main():
    load_dotenv()
    images_dir = os.getenv('IMAGES_DIR', default=os.path.join('', 'images'))
    os.makedirs(images_dir, exist_ok=True)
    nasa_token = os.getenv('NASA_TOKEN', default='DEMO_KEY')
    parser = argparse.ArgumentParser(description='Script fetches spacex\'s launch by ID')
    parser.add_argument('-ad', '--apod_day', default=None)
    args = parser.parse_args()
    load_apod_pictures(images_dir, nasa_token, args.apod_day)


if __name__ == '__main__':
    main()
