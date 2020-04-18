from pathlib import Path
import requests


def download_file(url, path: Path):
    response = requests.get(url)
    response.raise_for_status()
    path.write_bytes(response.content)