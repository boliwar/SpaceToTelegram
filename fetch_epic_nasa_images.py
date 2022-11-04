import library_for_space_photo as lsp
import requests
import argparse
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


def get_epic_nasa_pictures(nasa_api_key, directory, photo_date):
    payload = {"api_key": nasa_api_key}

    response = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{datetime.strftime(photo_date, '%Y-%m-%d')}",
                            timeout=30, params=payload)
    response.raise_for_status()
    current_date_url = datetime.strftime(photo_date, '%Y/%m/%d')
    picture_urls = [f"https://api.nasa.gov/EPIC/archive/natural/{current_date_url}/png/{picture_tuple['image']}.png"
                    for picture_tuple in response.json()]

    lsp.download_pictures(picture_urls, directory, payload)


def create_parser():
    parser = argparse.ArgumentParser(description='Function for load images from NASA EPIC.')
    parser.add_argument('date', type=str, nargs='?',
                        default=datetime.strftime(datetime.now() - timedelta(days=1), '%d.%m.%Y'),
                        help="Specify the date of the required images in the format dd.mm.yyyy. "
                             "The default is yesterday's date.")
    return parser


def main():
    parser = create_parser()
    command_line_arguments = parser.parse_args()
    load_dotenv()
    directory = os.environ['DIRECTORY_FOR_IMAGES']
    nasa_api_key = os.environ['NASA_API_KEY']
    full_path_images = lsp.get_dir_for_img(directory)

    try:
        photo_date = datetime.strptime(command_line_arguments.date, '%d.%m.%Y')
        get_epic_nasa_pictures(nasa_api_key, full_path_images, photo_date)
    except ValueError:
        print('Please, use date format dd.mm.yyyy')


if __name__ == "__main__":
    main()
