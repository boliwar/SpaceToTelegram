import requests
import os
import urllib
from pathlib import Path


def get_picture(url, filename, payload=None):
    response = requests.get(url, params=payload)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def download_pictures(picture_urls, directory, payload=None):
    for url in picture_urls:
        url_components = urllib.parse.urlparse(url)
        file_path, file_name = os.path.split(url_components.path)
        get_picture(url, Path(directory, file_name), payload)


def get_dir_for_img(directory):
    full_path = Path(Path.cwd(), directory)
    os.makedirs(full_path, exist_ok=True)
    return full_path
