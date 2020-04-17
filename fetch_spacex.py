import requests
from pathlib import Path

IMAGES_DIRECTORY = 'images/'


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


def download_file(url, path: Path):
    response = requests.get(url)
    response.raise_for_status()
    path.write_bytes(response.content)


def main():
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
