from pathlib import Path
import os
from PIL import Image
from instabot import Bot
from dotenv import load_dotenv
import random

Image.MAX_IMAGE_PIXELS = 900000000
IMAGES_DIRECTORY = 'images/'
INSTAGRAM_IMAGES_DIRECTORY = 'images_instagram/'


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


def get_proportional_size(width, height, max_size=1080):
    if max(width, height) > max_size:
        resize_ratio = max_size / max(width, height)
        width *= resize_ratio
        height *= resize_ratio
    return width, height


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


def main():
    load_dotenv()
    username = os.getenv('INSTAGRAM_USERNAME'),
    password = os.getenv('INSTAGRAM_PASSWORD')

    create_images_for_instagram()
    post_images_to_instagram(username, password)
