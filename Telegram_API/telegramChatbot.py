#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import datetime
import logging
from telegram import Bot,Update

token = "6297598995:AAF1kW0FinpGn737xiag1ESOtVUWZUQfTpA"

def start(update, context):
    logging.info('>>> start')
    context.bot.send_message(chat_id=update.effective_chat.id, text='환영합니다')

def stop(update, context):
    logging.info('>>> stop')
    context.bot.send_message(chat_id=update.effective_chat.id, text='종료합니다')

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response.json()

def message_handler(update, context):
    msgtext = update.message.text
    ct_id = update.effective_chat.id
    logging.info(msgtext)
    context.bot.send_message(chat_id=ct_id, text=msgtext)

def main():
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

