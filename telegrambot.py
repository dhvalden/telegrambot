#!/usr/bin/env python3

import logging
import subprocess
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from functools import wraps

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
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Hola/Hello/Hallo I'm a bot that can check the status of a Virtual Machine!")

@restricted
def addKeywords(update, context):
    keywords = context.args
    with open("/home/daniel/keywords.txt", "a") as o:
        for word in keywords:
            print(word)
            o.write(word + "\n")
    with open("/home/daniel/keywords.txt", "r") as f:
        filekeys = f.read().splitlines()
    context.bot.send_message(chat_id=update.message.chat_id, text=filekeys)


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand that command.")


@restricted
def status(update, context):
    response = subprocess.run(["sudo", "service", "tweet_collector", "status"], stdout=subprocess.PIPE)
    statusd = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=statusd)


@restricted
def ckeywords(update, context):
    response = subprocess.run(["cat", "home/daniel/envs/tweet_collector/keywords"], stdout=subprocess.PIPE)
    keywords = str(response.stdout, encoding="utf-8")
    context.bot.send_message(chat_id=update.message.chat_id, text=keywords)


def main():
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    addkeywords_handler = CommandHandler('add', addKeywords)
    dispatcher.add_handler(addkeywords_handler)

    status_handler = CommandHandler('status', status)
    dispatcher.add_handler(status_handler)

    keywords_handler = CommandHandler('keywords', ckeywords)
    dispatcher.add_handler(keywords_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()


if __name__ == '__main__':
	main()
