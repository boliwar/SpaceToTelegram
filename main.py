import requests
import os
import urllib
from dotenv import load_dotenv
from datetime import datetime, timedelta

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


def get_spacex_list_pictures(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def get_nasa_list_pictures(count):
    nasa_api_key = os.environ['nasa_api_key']
    payload = {"api_key": nasa_api_key, "count": count}
    feed = requests.get(f'https://api.nasa.gov/planetary/apod', timeout=30, params=payload)
    feed.raise_for_status()
    list_pictures = []
    for slice_picture in feed.json():
        list_pictures.append(slice_picture['url'])
    return  list_pictures


def get_file_name(url):
    url_components = urllib.parse.urlparse(url)
    tuple_name=os.path.split(url_components.path)
    return tuple_name[1]


def get_epic_nasa_pictures(directory, photo_date = None):
    nasa_api_key = os.environ['nasa_api_key']
    payload = {"api_key": nasa_api_key}

    if photo_date is None:
        photo_date = datetime.now() - timedelta(days=1)

    feed = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{datetime.strftime(photo_date, '%Y-%m-%d')}", timeout=30, params=payload)
    feed.raise_for_status()
    currdateurl = datetime.strftime(photo_date, '%Y/%m/%d')
    list_url_pictures=[]
    for corteg in feed.json():
        fname = corteg['image']
        list_url_pictures.append(f"https://api.nasa.gov/EPIC/archive/natural/{currdateurl}/png/{fname}.png")
    dowload_list_pictures(list_url_pictures, directory, payload)


def fetch_spacex_last_launch(directory):
    pictures_url = f"https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a"

    list_url_pictures = get_spacex_list_pictures(pictures_url)
    dowload_list_pictures(list_url_pictures, directory)


def fetch_nasa_pictures(directory, count):
    list_url_pictures = get_nasa_list_pictures(count)
    dowload_list_pictures(list_url_pictures, directory)


def main():
    load_dotenv()
    directory = '.\images'
    if not os.path.exists(directory):
        os.mkdir(directory)

    # fetch_spacex_last_launch(directory)
    fetch_nasa_pictures(directory, 20)
    get_epic_nasa_pictures(directory)

if __name__ == "__main__":
    main()