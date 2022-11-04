import library_for_space_photo as lsp
import requests
import argparse
from dotenv import load_dotenv
import os


def get_nasa_picture_urls(nasa_api_key, count):
    payload = {"api_key": nasa_api_key, "count": count}
    feed = requests.get(f'https://api.nasa.gov/planetary/apod', timeout=30, params=payload)
    feed.raise_for_status()
    picture_urls = [slice_picture['url'] for slice_picture in feed.json()]

    return picture_urls


def fetch_nasa_pictures(nasa_api_key, directory, count):
    picture_urls = get_nasa_picture_urls(nasa_api_key, count)
    lsp.download_pictures(picture_urls, directory)


def create_parser():
    parser = argparse.ArgumentParser(description='Function for load images from NASA APOD.')
    parser.add_argument('count', type=int, nargs='?', default=5,
                        help='Input how much pictures must be load on one session. Default 5.')
    return parser


def main():
    parser = create_parser()
    command_line_arguments = parser.parse_args()
    count = command_line_arguments.count
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    directory = os.environ['DIRECTORY_FOR_IMAGES']
    full_path_images = lsp.get_dir_for_img(directory)

    fetch_nasa_pictures(nasa_api_key, full_path_images, count)


if __name__ == "__main__":
    main()
