import telegram
import os
from os.path import isfile, join
from dotenv import load_dotenv
import library_for_space_photo as lsp


def main():
    load_dotenv()
    token = os.environ['TOKEN']
    chat_id = os.environ['chat_id']
    directory = lsp.get_dir_for_img()
    bot = telegram.Bot(token=token)
    media_list=[]
    for object in os.listdir(directory):
        if isfile(f"{directory}\\{object}"):
            media_list.append(f"{directory}\\{object}")
            break
    
    bot.send_document(chat_id=chat_id, document=open(media_list[0], 'rb'))

if __name__ == "__main__":
    main()