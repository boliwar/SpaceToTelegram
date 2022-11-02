import library_for_space_photo as lsp
import requests
import argparse
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

def get_epic_nasa_pictures(directory, photo_date):
    nasa_api_key = os.environ['nasa_api_key']
    payload = {"api_key": nasa_api_key}

    feed = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{datetime.strftime(photo_date, '%Y-%m-%d')}", timeout=30, params=payload)
    feed.raise_for_status()
    curent_date_url = datetime.strftime(photo_date, '%Y/%m/%d')
    list_url_pictures=[]
    for corteg in feed.json():
        fname = corteg['image']
        list_url_pictures.append(f"https://api.nasa.gov/EPIC/archive/natural/{curent_date_url}/png/{fname}.png")
    lsp.dowload_list_pictures(list_url_pictures, directory, payload)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('date', nargs='?')
    return parser


def main():
    load_dotenv()
    directory = lsp.get_dir_for_img()
    parser = create_parser()
    command_line_arguments = parser.parse_args()

    if command_line_arguments.date is None:
        photo_date = datetime.now() - timedelta(days=1)
    else:
        try:
            photo_date = datetime.strptime(command_line_arguments.date, '%d.%m.%Y')
        except:
            print('Please, use date format dd.mm.yyyy')
            exit(0)

    get_epic_nasa_pictures(directory, photo_date)


if __name__ == "__main__":
    main()