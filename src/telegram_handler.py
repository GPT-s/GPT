import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup as MU 
from telepot.namedtuple import InlineKeyboardButton as BT 
import time
import datetime
import logging
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup,Update,InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()

teltoken = os.environ.get('teltoken')

token = teltoken


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
    # context.bot.send_message(chat_id=ct_id, text=msgtext)

    if msgtext == "naver":
        webpage="https://www.naver.com"
        context.bot.send_message(chat_id=update.effective_chat.id, text=webpage)
    elif msgtext == "google":
        webpage="https://www.google.com"
        context.bot.send_message(chat_id=update.effective_chat.id, text=webpage)
    elif msgtext == "youtube":
        webpage="https://www.youtube.com"
        context.bot.send_message(chat_id=update.effective_chat.id, text=webpage)
    

def favorites(update, context):
    message_text = update.message.text
    search_query = message_text.lower().replace('/favorites ', '')
    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])
    if len(favorites_list) < 5:
        favorites_list.append(search_query)
        user_data['favorites_list'] = favorites_list
    
    keyboard = []
    if favorites_list:
        for favorite in favorites_list:
            button = KeyboardButton(favorite)
            keyboard.append([button])
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(f'{search_query}등록', reply_markup=reply_markup)
    
    
    # buttons = []
    # for favorite in favorites_list:
    #     button = InlineKeyboardButton(favorite, callback_data=favorite)
    #     buttons.append(button)
    # update.message.reply_text('⭐즐겨찾기', reply_markup=InlineKeyboardMarkup([buttons]))

def remove_favorite(update, context):
    message_text = update.message.text
    remove_query = message_text.lower().replace('/remove ', '')
    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])
    if remove_query in favorites_list:
        favorites_list.remove(remove_query)
        user_data['favorites_list'] = favorites_list
    
    keyboard = []
    if favorites_list:
        for favorite in favorites_list:
            button = KeyboardButton(favorite)
            keyboard.append([button])
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(f'{remove_query}제거', reply_markup=reply_markup)
    # buttons = []
    # for favorite in favorites_list:
    #     button = InlineKeyboardButton(favorite, callback_data=favorite)
    #     buttons.append(button)
    # update.message.reply_text('⭐즐겨찾기', reply_markup=InlineKeyboardMarkup([buttons]))

def favoriteslist(update, context):
    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])
    buttons = []
    for favorite in favorites_list:
        button = InlineKeyboardButton(favorite, callback_data=favorite)
        buttons.append(button)
    update.message.reply_text('⭐즐겨찾기', reply_markup=InlineKeyboardMarkup([buttons]))

def button_callback(update, context):
    query = update.callback_query
    data = query.data
    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])
    newsdate = "뉴스데이터가 들어갑니다"
    stockindexdate = "지수데이터가 들어갑니다"
    if data in favorites_list:
        query.answer()
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text=f"선택한 주식: {data}")
        stock_button = InlineKeyboardButton("주식", callback_data="stock")
        index_button = InlineKeyboardButton("지수", callback_data="index")
        buttons = [stock_button, index_button]
        reply_markup = InlineKeyboardMarkup([buttons])
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="원하는 기능을 선택하세요.",
                                 reply_markup=reply_markup)
        
    elif data == "stock":
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text=newsdate)
        
    elif data == "index":
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text=stockindexdate)


def on_keyboard_button_pressed(update, context):

    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])
# GUI 버튼 생성
    stock_button = InlineKeyboardButton(text='주식', callback_data='stock')
    index_button = InlineKeyboardButton(text='지수', callback_data='index')
    
    # GUI 버튼을 포함한 InlineKeyboardMarkup 생성
    reply_markup = InlineKeyboardMarkup([[stock_button, index_button]])
    
    # 채팅방에 GUI 버튼 전송
    for favorite in favorites_list:
        update.message.reply_text(favorite, reply_markup=reply_markup)
    # keyboard = []
    # 
    # if favorites_list:
    #     for favorite in favorites_list:
    #         button = KeyboardButton(favorite)
    #         keyboard.append([button])
    #         stock_button = InlineKeyboardButton(text='주식', callback_data='stock')
    #         index_button = InlineKeyboardButton(text='지수', callback_data='index')
    #         reply_markup = InlineKeyboardMarkup([[stock_button, index_button]])
    # reply_markup1 = ReplyKeyboardMarkup(keyboard)
    # update.message.reply_text(f'{search_query}등록', reply_markup=reply_markup)
    # update.message.reply_text('KeyboardButton을 누르면 나타나는 GUI 버튼입니다.', reply_markup=reply_markup)




def main():
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(CommandHandler('favorites', favorites, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler('remove', remove_favorite, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler('favoriteslist', favoriteslist))
    updater.dispatcher.add_handler(CommandHandler('list', favoriteslist))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(f'^삼성$'), on_keyboard_button_pressed))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()