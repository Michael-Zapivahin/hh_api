import requests
import url_processing
import argparse
import os
import uuid

from dotenv import load_dotenv


def fetch_spacex_launch(image_dir, start_id):
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{start_id}')
    response.raise_for_status()
    links = response.json()['links']
    for link in links:
        if link == 'patch':
            url = links[link]['small']
            path = os.path.join(image_dir, f'spacex_{uuid.uuid4()}')
            filename = f'{path}.{url_processing.get_file_type(url)}'
            url_processing.download_image(url, filename)


def main():
    load_dotenv()
    images_dir = os.getenv('IMAGES_DIR', default=os.path.join('', 'images'))
    os.makedirs(images_dir, exist_ok=True)
    parser = argparse.ArgumentParser(description='Script fetches spacex\'s launch by ID')
    parser.add_argument('-id', '--start_id', default='latest')
    args = parser.parse_args()
    fetch_spacex_launch(images_dir, args.start_id)


if __name__ == '__main__':
    main()
