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
import openai
from dotenv import load_dotenv
import os

load_dotenv()

teltoken = os.environ.get('teltoken')
token = teltoken

GPTAPI = os.environ.get('GPTAPI')
OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY
model = "gpt-3.5-turbo"

# /start 커맨드 기능
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text='주식챗봇 시작을 환영합니다')
    return chat_id

# /help 커맨드 기능
def help(update, context):
    helptext = "1. '/favorites 주식이름' 으로 키보드버튼을 추가할 수 있습니다.\n\
2. '/remove 주식이름' 으로 키보드 버튼을 삭제할 수 있습니다.\n\
3. 키보드 버튼 클릭시\n    해당 버튼에 대한 뉴스 / 지수 버튼 메세지가 전송됩니다.\n\
4. 뉴스 또는 지수 버튼 클릭시\n    버튼에 해당하는 내용의 메세지가 전송됩니다.\n\
5. 특정사이트 링크\n\
    '네이버' 입력시 네이버 링크가 전송됩니다.\n\
    '구글' 입력시 네이버 링크가 전송됩니다.\n\
    '야후파이낸스' 입력시 네이버 링크가 전송됩니다.\n\
    '인베스팅' 입력시 네이버 링크가 전송됩니다.\n\
    '유튜브' 입력시 네이버 링크가 전송됩니다."
    context.bot.send_message(chat_id=update.effective_chat.id, text=helptext)

# 메세지 보내는기능
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response.json()


# 마지막 텍스트 가져오는 기능
def message_text(token):
    url = f"https://api.telegram.org/{token}/getUpdates"
    response = requests.get(url)
    response_dict = response.json()
    last_message = response_dict['result'][-1]['message']['text']
    return last_message



# 즐겨찾기 등록하는 커맨드 /favorites 등록할커맨드
def favorites(update, context):
    message_text = update.message.text
    if not message_text.lower().startswith('/favorites '):
        return
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
    context.user_data['keyboard'] = keyboard
    selectbuttons = []
    if favorites_list:
        for favorite in favorites_list:
            stock_button = InlineKeyboardButton(text=f'{favorite}주식', callback_data=f'stock_{favorite}')
            index_button = InlineKeyboardButton(text=f'{favorite}지수', callback_data=f'index_{favorite}')
            selectbuttons.append([stock_button, index_button])
    context.user_data['selectbuttons'] = selectbuttons   
    update.message.reply_text(f'{search_query}등록', reply_markup=reply_markup)
      

def in_subscribe(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="구독 처리가 완료되었습니다.")
    return chat_id

def out_subscribe(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="구독 취소가 완료되었습니다.")
    return chat_id

   
# 마지막 텍스트에 반응하는 기능
def message_handler(update, context):
    msgtext = update.message.text
    chat_id = update.effective_chat.id
    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])
    selectbuttons = user_data.get('selectbuttons', [])
    logging.info(msgtext)
    
    if msgtext == "네이버":
        webpage="https://www.naver.com"
        context.bot.send_message(chat_id=chat_id, text=webpage)
    elif msgtext == "구글":
        webpage="https://www.google.com"
        context.bot.send_message(chat_id=chat_id, text=webpage)
    elif msgtext == "유튜브":
        webpage="https://www.youtube.com"
        context.bot.send_message(chat_id=chat_id, text=webpage)
    elif msgtext == "야후파이낸스":
        webpage="https://finance.yahoo.com"
        context.bot.send_message(chat_id=chat_id, text=webpage)
    elif msgtext == "인베스팅":
        webpage="https://kr.investing.com"
        context.bot.send_message(chat_id=chat_id, text=webpage)
    else:
        for favorite_idx, favorite in enumerate(favorites_list):
            if msgtext == favorite:
                reply_markups = None
                if favorite_idx < len(selectbuttons):
                    reply_markups = InlineKeyboardMarkup([selectbuttons[favorite_idx]])
                update.message.reply_text(f'{favorite}', reply_markup=reply_markups)
                break
        else:
            gptquery = msgtext
            messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": gptquery}
                        ]
            response = openai.ChatCompletion.create(
                        model=model,
                        messages=messages
                        )
            answer = response['choices'][0]['message']['content']
            context.bot.send_message(chat_id=chat_id, text=answer)
           
                
# 즐겨찾기 삭제하는 커맨드  /remove 삭제할종목
def remove_favorite(update, context):
    message_text = update.message.text
    if not message_text.lower().startswith('/remove '):
        return
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
    elif favorites_list == []:
        button = KeyboardButton("등록해주세요")
        keyboard.append([button])
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(f'{remove_query}제거', reply_markup=reply_markup)


def on_callback_query(update, context):
    query = update.callback_query
    query_data = query.data
    user_data = context.user_data
    favorites_list = user_data.get('favorites_list', [])

    for favorite in favorites_list:
        if query_data == f'stock_{favorite}':
            context.bot.send_message(chat_id=query.message.chat_id,
                                                text=f"{favorite}주식")

        elif query_data == f'index_{favorite}':
            context.bot.send_message(chat_id=query.message.chat_id,
                                                text=f"{favorite}지수")
    

def main():
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('sub', in_subscribe))
    updater.dispatcher.add_handler(CommandHandler('nosub', out_subscribe))
    updater.dispatcher.add_handler(CommandHandler('favorites', favorites, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler('remove', remove_favorite, pass_user_data=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, on_callback_query))
    updater.dispatcher.add_handler(CallbackQueryHandler(on_callback_query))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()