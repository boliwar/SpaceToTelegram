import time
import telegram
import os
from os.path import isfile, join
from dotenv import load_dotenv
import library_for_space_photo as lsp
import random
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pause', nargs='?')
    return parser

def main():
    load_dotenv()
    token = os.environ['TOKEN']
    chat_id = os.environ['chat_id']
    directory = lsp.get_dir_for_img()
    bot = telegram.Bot(token=token)
    parser = create_parser()
    command_line_arguments = parser.parse_args()
    pause_hour = command_line_arguments.pause if command_line_arguments.pause else 4
    media_list=[]

    while True:
        for address, dirs, files in os.walk(directory):
            for name in files:
                media_list.append(os.path.join(address, name))

        while True:
            fname = random.choices(media_list)
            bot.send_document(chat_id=chat_id, document=open(fname[0], 'rb'))
            media_list.remove(fname[0])
            time.sleep(pause_hour*60*60)
            if not media_list:
                break

if __name__ == "__main__":
    main()