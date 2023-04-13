
import requests
import datetime
import os
import url_processing

from dotenv import load_dotenv


def load_epic_pictures(image_dir, nasa_token):
    url = 'https://epic.gsfc.nasa.gov/api/natural'
    payload = {
        'api_key': nasa_token
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    links = response.json()
    for link in links:
        image_name = link['image']
        image_date = datetime.datetime.strptime(link['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png'
        file_name = f'{os.path.join(image_dir, image_name)}.png'
        url_processing.download_image(image_url, file_name, payload)



def main():
    load_dotenv()
    images_dir = os.getenv('IMAGES_DIR', default=os.path.join('', 'images'))
    os.makedirs(images_dir, exist_ok=True)
    nasa_token = os.getenv('NASA_TOKEN', default='DEMO_KEY')
    load_epic_pictures(images_dir, nasa_token)


if __name__ == '__main__':
    main()
