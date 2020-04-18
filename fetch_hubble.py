import requests
from pathlib import Path
from scripts import download_file

IMAGES_DIRECTORY = 'images/'


def fetch_hubble():
    host = 'http://hubblesite.org'
    method = '/api/v3/images/all'
    url = host + method
    response = requests.get(url)

    for image_data in response.json():
        image_id = image_data['id']
        download_hubble_img(image_id)


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
    download_file(image_url, path)


def get_extension_file(url):
    return url.split('.')[-1]


def main():
    fetch_hubble()


if __name__ == '__main__':
    main()
