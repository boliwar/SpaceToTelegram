import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = os.environ['TOKEN']
    chat_id = os.environ['chat_id']
    bot = telegram.Bot(token=token)
    #print(bot.get_me())
    # updates = bot.get_updates()
    # print(updates[0])
    bot.send_message(text='Hi John!', chat_id=chat_id)

if __name__ == "__main__":
    main()