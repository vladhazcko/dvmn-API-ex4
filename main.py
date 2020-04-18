import requests
from pathlib import Path
import os
from PIL import Image
from instabot import Bot
from dotenv import load_dotenv
import random
from scripts import download_file

Image.MAX_IMAGE_PIXELS = 900000000
IMAGES_DIRECTORY = 'images/'
INSTAGRAM_IMAGES_DIRECTORY = 'images_instagram/'


def main():
    load_dotenv()
    username = os.getenv('INSTAGRAM_USERNAME'),
    password = os.getenv('INSTAGRAM_PASSWORD')

    fetch_spacex_last_launch()
    fetch_hubble()
    create_images_for_instagram()
    post_images_to_instagram(username, password)


def fetch_spacex_last_launch(directory=IMAGES_DIRECTORY):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    while True:
        parameter = 'latest'
        method_url = f'https://api.spacexdata.com/v3/launches/{parameter}'
        response = requests.get(method_url)
        response.raise_for_status()
        response_dict = response.json()
        try:
            images_urls = response_dict['links']['flickr_images']
            if not len(images_urls):
                raise Exception('Images list is empty')
        except Exception or KeyError:
            parameter = response_dict['flight_number']
        else:
            break

    for image_number, image_url in enumerate(images_urls):
        image_path = directory / f'spacex{image_number}.jpg'
        download_file(image_url, image_path)


def fetch_hubble():
    host = 'http://hubblesite.org'
    method = '/api/v3/images/all'
    url = host + method
    response = requests.get(url)

    for image_data in response.json():
        image_id = image_data['id']
        download_hubble_img(image_id)


def get_extension_file(url):
    return url.split('.')[-1]


def download_hubble_img(id, directory=IMAGES_DIRECTORY):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    host = 'http://hubblesite.org'
    method = '/api/v3/image/'
    request_url = host + method + str(id)

    response = requests.get(request_url)
    response.raise_for_status()
    image_url = 'http:' + response.json()['image_files'][-1]['file_url']
    extension = get_extension_file(image_url)
    path = directory / f'{id}.{extension}'
    print(f'Download image: id {id}')
    download_file(image_url, path)


def get_proportional_size(width, height, max_size=1080):
    if max(width, height) > max_size:
        resize_ratio = max_size / max(width, height)
        width *= resize_ratio
        height *= resize_ratio
    return width, height


def create_images_for_instagram():

    images_files = os.listdir(IMAGES_DIRECTORY)
    directory = Path(INSTAGRAM_IMAGES_DIRECTORY)
    directory.mkdir(parents=True, exist_ok=True)
    for image_file in images_files:
        image_path = IMAGES_DIRECTORY + image_file

        try:
            image = Image.open(image_path)
        except OSError:
            continue

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        new_size = get_proportional_size(*image.size)
        new_image = image
        new_image.thumbnail(new_size)

        new_image_file = image_file.split('.')[0] + '.jpg'
        new_image_path = INSTAGRAM_IMAGES_DIRECTORY + new_image_file
        new_image.save(new_image_path, format='JPEG')


def post_images_to_instagram(username, password):
    files_images = os.listdir(INSTAGRAM_IMAGES_DIRECTORY)
    with open('space_quotes.txt', 'r', encoding='utf-8') as file:
        quotes = file.read().split('\n')

    bot = Bot()
    bot.login(
        is_threaded=False,
        username=username,
        password=password
    )
    for file_image in files_images:
        path = INSTAGRAM_IMAGES_DIRECTORY + file_image
        bot.upload_photo(path, caption=random.choice(quotes))


if __name__ == '__main__':
    main()
