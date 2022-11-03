import library_for_space_photo as lsp
import requests
import argparse
from dotenv import load_dotenv
import os


def get_spacex_pictures_urls(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def fetch_spacex_pictures(directory, launch_id):
    pictures_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"

    picture_urls = get_spacex_pictures_urls(pictures_url)
    lsp.download_pictures(picture_urls, directory)


def create_parser():
    parser = argparse.ArgumentParser(description='Function for load images from SpaceX launch.')
    parser.add_argument('id', type=str, nargs='?', default='latest',
                        help='Use to specify id for the desired launch. The last one is selected by default.')
    return parser


def main():
    parser = create_parser()
    command_line_arguments = parser.parse_args()
    launch_id = command_line_arguments.id
    load_dotenv()
    directory = os.environ['directory_for_images']
    full_path_images = lsp.get_dir_for_img(directory)

    fetch_spacex_pictures(full_path_images, launch_id)


if __name__ == "__main__":
    main()
