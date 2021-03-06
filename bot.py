#!/usr/bin/python3

import os
import re
import logging
from telegram.ext import Updater, CommandHandler, run_async
from xvideos import choose_random_porn_comment, XvideosException

def log_username(update):
    try:
        username = update.effective_user.username
        if update['message']['chat']['type'] == 'group':
            group = update['message']['chat']['title']
            logging.info(f'@{username} {group}')
        else:
            logging.info(f'@{username}')
    except KeyError:
        logging.warning('Could not read username')

@run_async
def comentario(bot, update):
    log_username(update)

    def send(message):
        bot.send_message(chat_id=update.message.chat_id, text=message)

    send('Vou procurar um comentario aqui, perae...')

    try:
        author, content, title = choose_random_porn_comment()
        send(f'{author} comentou o seguinte:\n{content}\n\nVi isso no video:\n{title}')
    except XvideosException as ex:
        send(f'Erro!\n\n{ex}')
        logging.error(f'{ex}')
    except Exception as ex:
        logging.error(f'{ex}')
        send('Houve um erro! Entre em contato com @GabrielBlank no Telegram')

@run_async
def comment(bot, update):
    log_username(update)

    def send(message):
        bot.send_message(chat_id=update.message.chat_id, text=message)

    match = re.match(r'^\/comment\s(([a-z]+\s)*[a-z]+)$', update.message.text, re.IGNORECASE)

    if not match:
        send('send "/comment" followed by a search term. Example:\n\n/comment big dick')
        return

    send('Searching... Hang on!')

    search_term = match.group(1).replace(' ', '+')

    try:
        author, content, title = choose_random_porn_comment(search_term)
        send(f'Comment by {author}:\n{content}\n\nI saw it in the video:\n{title}')
    except XvideosException as ex:
        logging.error(f'{ex}')
        send(f'There was an error!\n\n{ex}')
    except Exception as ex:
        logging.error(f'{ex}')
        send('There was an error! Contact @GabrielBlank on Telegram')

def start(bot, update):
    log_username(update)
    update.message.reply_text(text='Ola!\n\nEscreva /comentario para eu te mostrar algum comentario do meu site favorito!')

def main():
    logging.basicConfig(
        filename='/var/log/bot-telegram-xvideos.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S')

    try:
        updater = Updater(os.environ['BOT_TELEGRAM_XVIDEOS_TOKEN'])
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('comentario', comentario))
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('comment', comment))

        updater.start_polling()

        print('Running!')

        updater.idle()

        print()
    except Exception as ex:
        logging.critical(f'{ex}')

if __name__ == '__main__':
    main()
