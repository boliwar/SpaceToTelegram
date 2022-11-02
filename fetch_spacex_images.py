import library_for_space_photo as lsp
import requests
import argparse
from dotenv import load_dotenv


def get_spacex_list_pictures(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]

def fetch_spacex_launch(directory, launch_id):
    pictures_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"

    list_url_pictures = get_spacex_list_pictures(pictures_url)
    lsp.dowload_list_pictures(list_url_pictures, directory)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='?')
    return parser


def main():
    load_dotenv()
    directory = lsp.make_dir_for_img()
    parser = create_parser()
    command_line_arguments = parser.parse_args() # 5eb87d47ffd86e000604b38a
    launch_id = command_line_arguments.id if command_line_arguments.id else 'latest'
    fetch_spacex_launch(directory, launch_id)


if __name__ == "__main__":
    main()