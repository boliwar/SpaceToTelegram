import time
import telegram
import os
from dotenv import load_dotenv
import library_for_space_photo as lsp
import random
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Bot for load images to Telegram channel')
    parser.add_argument('pause', type=int, nargs='?', default=4,
                        help='Input how much hour must be between send messages. Default 4.')
    return parser


def main():
    parser = create_parser()
    command_line_arguments = parser.parse_args()
    timeout_hours = command_line_arguments.pause
    load_dotenv()
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    directory = os.environ['DIRECTORY_FOR_IMAGES']
    full_path_images = lsp.get_dir_for_img(directory)
    bot = telegram.Bot(token=tg_bot_token)

    media_files = []

    while True:
        for address, dirs, files in os.walk(full_path_images):
            for name in files:
                media_files.append(os.path.join(address, name))

        while True:
            file_name = random.choices(media_files)
            with open(file_name[0], 'rb') as fileload:
                bot.send_document(chat_id=tg_chat_id, document=fileload)
            media_files.remove(file_name[0])
            time.sleep(timeout_hours*60*60)
            if not media_files:
                break


if __name__ == "__main__":
    main()
