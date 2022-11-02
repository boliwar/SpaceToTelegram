import library_for_space_photo as lsp
import requests
import argparse
from dotenv import load_dotenv
import os

def get_nasa_list_pictures(count):
    nasa_api_key = os.environ['nasa_api_key']
    payload = {"api_key": nasa_api_key, "count": count}
    feed = requests.get(f'https://api.nasa.gov/planetary/apod', timeout=30, params=payload)
    feed.raise_for_status()
    list_pictures = []
    for slice_picture in feed.json():
        list_pictures.append(slice_picture['url'])
    return  list_pictures


def fetch_nasa_pictures(directory, count):
    list_url_pictures = get_nasa_list_pictures(count)
    lsp.dowload_list_pictures(list_url_pictures, directory)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('count', nargs='?')
    return parser


def main():
    load_dotenv()
    directory = lsp.make_dir_for_img()
    parser = create_parser()
    command_line_arguments = parser.parse_args()
    count = command_line_arguments.count if command_line_arguments.count else 5
    fetch_nasa_pictures(directory, count)


if __name__ == "__main__":
    main()