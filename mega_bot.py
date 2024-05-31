import os
from telegram.ext import Updater, CommandHandler
from mega import Mega
from dotenv import load_dotenv

# Load environment variables from config.env file
load_dotenv('config.env')

# Your bot token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Initialize Mega instance
mega = Mega()
m = mega.login(os.getenv('MEGA_EMAIL'), os.getenv('MEGA_PASSWORD'))

def start(update, context):
    update.message.reply_text('Hello! Use /count {mega link} to count files.')

def count_files_in_mega_link(url):
    files = m.get_files_from_link(url)
    return len(files)

def count(update, context):
    text = update.message.text.split()
    if len(text) != 2:
        update.message.reply_text('Usage: /count {mega link}')
        return

    url = text[1]
    if 'mega.nz' in url:
        try:
            file_count = count_files_in_mega_link(url)
            update.message.reply_text(f'There are {file_count} files in the MEGA link.')
        except Exception as e:
            update.message.reply_text(f'Error: {str(e)}')
    else:
        update.message.reply_text('Invalid link. Please provide a valid MEGA link.')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("count", count))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

