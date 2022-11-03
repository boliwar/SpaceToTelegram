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
        get_picture(url, Path(directory, get_file_name(url)), payload)


def get_file_name(url):
    url_components = urllib.parse.urlparse(url)
    tuple_name = os.path.split(url_components.path)
    return tuple_name[1]


def get_dir_for_img(directory):
    full_path = Path(Path.cwd(), directory)
    os.makedirs(full_path, exist_ok=True)
    return full_path
