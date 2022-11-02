import requests
import os
import urllib


def get_picture(url, filename, payload=None):
    if payload is None:
        response = requests.get(url)
    else:
        response = requests.get(url, params=payload)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def dowload_list_pictures(list_url_pictures, directory, payload=None):
    for url in list_url_pictures:
        get_picture(url, f"{directory}\\{get_file_name(url)}", payload)


def get_file_name(url):
    url_components = urllib.parse.urlparse(url)
    tuple_name=os.path.split(url_components.path)
    return tuple_name[1]


def get_dir_for_img():
    directory = f"{os.path.split(os.path.abspath(__file__))[0]}{os.environ['directory']}"
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory

