#!/usr/bin/env python3

import os
import logging
import subprocess
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from functools import wraps

LIST_OF_ADMINS = [757127759]

def read_keys(file_name, key_names):
    credentials = {}
    with open(file_name, "r") as f:
        text = f.read()
        keylist = text.replace("=", " ").split()
    for key in key_names:
        index = keylist.index(key)
        credentials[key] = keylist[index+1]
    return credentials


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def start(update, context):
    STARTMESSAGE = '''
    Hola/Hello/Hallo I'm the bot checking your data collection!
    '''
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=STARTMESSAGE)

@restricted
def addKeywords(update, context):
    KEYWORDS = "/home/daniel/envs/tweet_collector/keywords"
    new_keywords = context.args
    with open(KEYWORDS, "a") as o:
        for word in new_keywords:
            print(word)
            o.write(word + "\n")
    with open(KEYWORDS, "r") as f:
        filekeys = f.read().splitlines()
    context.bot.send_message(chat_id=update.message.chat_id, text=filekeys)


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand that command.")


@restricted
def status(update, context):
    response = subprocess.run(["sudo", "service", "tweet_collector", "status"],
                              stdout=subprocess.PIPE)
    statusd = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=statusd)


@restricted
def stop(update, context):
    response = subprocess.run(["sudo", "service", "tweet_collector", "stop"],
                              stdout=subprocess.PIPE)
    statusd = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=statusd)


@restricted
def start_service(update, context):
    response = subprocess.run(["sudo", "service", "tweet_collector", "start"],
                              stdout=subprocess.PIPE)
    statusd = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=statusd)


@restricted
def restart(update, context):
    response = subprocess.run(["sudo", "service", "tweet_collector", "restart"],
                              stdout=subprocess.PIPE)
    statusd = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=statusd)


@restricted
def ckeywords(update, context):
    KEYWORDS = "/home/daniel/envs/tweet_collector/keywords"
    response = subprocess.run(["cat", KEYWORDS], stdout=subprocess.PIPE)
    keywords = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=keywords)


def main():
    PATH = os.path.dirname(os.path.realpath(__file__))
    KEYS = PATH + "/keys"

    credentials = read_keys(KEYS, ["TOKEN"])
    
    updater = Updater(token=credentials["TOKEN"], use_context=True)

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    addkeywords_handler = CommandHandler('add', addKeywords)
    dispatcher.add_handler(addkeywords_handler)

    status_handler = CommandHandler('status', status)
    dispatcher.add_handler(status_handler)

    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)

    start_s_handler = CommandHandler('startService', start_service)
    dispatcher.add_handler(start_s_handler)

    restart_handler = CommandHandler('restart', restart)
    dispatcher.add_handler(restart_handler)

    keywords_handler = CommandHandler('keywords', ckeywords)
    dispatcher.add_handler(keywords_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()


if __name__ == '__main__':
	main()
