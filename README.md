# Posting NASA images to telegram

Program downloads pictures from NASA resources

## How to install

Python3 should already be installed. 
Use pip or pip3, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```

## How to view log. 

Open the log file: `telegram_log.txt`

## Program uses an environment variable

#### Variables:

`NASA_TOKEN` [NASA developer key](https://api.nasa.gov/#signUp), `default='DEMO_KEY`

`IMAGES_DIR` directory for saving your pictures, `default='images'`

`TG_BOT_TOKEN`  [bot token](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

`TG_CHAT_ID` [chat's ID for send messages and pictures](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)

`TG_DELAY` message interval in seconds, `default='14400'`

`TG_MAX_SIZE` maximum image's size to upload to the Telegram, `default='3145728'` bytes, larger images will not be loaded. 



## How to run scripts

#### Download a image of the day: 

**URL** : `https://api.nasa.gov/planetary/apod`

**URL Parameters** : `api_key=[string]` where `api_key` is  [NASA developer key](https://api.nasa.gov/#signUp) for test `api_key=DEMO_KEY`
 
**Parameters**: `-ad` day of the image (Y-m-d)
```
python nasa_apod_images.py -ad 2023-01-01
```

#### Get one launch

**URL** : `https://api.spacexdata.com/v5/launches/:id`

**Parameters** : `id=[string]` where `id` is the ID of the launch

**Auth required** : `False`

```
python spacex_images.py -id 62dd70d5202306255024d139
``` 

#### Get EPIC images from collection Earth Polychromatic Imaging Camera (EPIC)

You should sign up for a [NASA developer key](https://api.nasa.gov/#signUp)

API demo key 'api_key=DEMO_KEY'

[Example](https://api.nasa.gov/EPIC/archive/natural/2019/05/30/png/epic_1b_20190530011359.png?api_key=DEMO_KEY)

```
python nasa_epic_images

```

## The aim of the project 
The code is written for educational purposes on the online course for web developers [Devman практика Python](https://dvmn.org/)
