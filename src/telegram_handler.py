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
from src.database import DataBase
import re
from src.stock_idx import StockData
from src.translator_deepl import DeeplTranslator
from src.livecrawler import LiveCrawler
from src.gpt import get_summary_list,summarize

load_dotenv()

teltoken = os.environ.get('teltoken')
token = teltoken

GPTAPI = os.environ.get('GPTAPI')
OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY
model = "gpt-3.5-turbo"
database = DataBase()




class TelegramHandler:
    
    def __init__(self):
        self.token = token
        self.updater = Updater(token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', TelegramHandler.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', TelegramHandler.help))
        self.updater.dispatcher.add_handler(CommandHandler('in', TelegramHandler.in_subscribe))
        self.updater.dispatcher.add_handler(CommandHandler('out', TelegramHandler.out_subscribe))
        self.updater.dispatcher.add_handler(CommandHandler('f', TelegramHandler.favorites, pass_user_data=True))
        self.updater.dispatcher.add_handler(CommandHandler('d', TelegramHandler.remove_favorite, pass_user_data=True))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), TelegramHandler.message_handler, pass_user_data=True))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, TelegramHandler.on_callback_query))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(TelegramHandler.on_callback_query))
        self.updater.start_polling()

    # /start 커맨드 기능
    def start(update, context):        
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=update.effective_chat.id, text='주식챗봇 시작을 환영합니다') 
        database.insert_user(chat_id, "N")

        return chat_id
    

    # /help 커맨드 기능
    def help(update, context):
        helptext = """1. '/f 주식이름'으로 키보드버튼을 추가할 수 있습니다.
        2. '/d 주식이름'으로 키보드 버튼을 삭제할 수 있습니다.
        3. 키보드 버튼 클릭시 해당 버튼에 대한 뉴스 / 차트 버튼 메세지가 전송됩니다.
        4. 뉴스 또는 차트 버튼 클릭시 버튼에 해당하는 내용의 메세지가 전송됩니다.
        5. /in 커맨드입력으로 8시30분 15시30분에 발송되는 주식뉴스를 구독할 수 있습니다.
        6. /out 커맨드입력으로 8시30분 15시30분에 발송되는 주식뉴스를 구독 취소할 수 있습니다.
        7. 특정사이트 링크
        '네이버' 입력시 네이버 링크가 전송됩니다.
        '구글' 입력시 네이버 링크가 전송됩니다.
        '야후파이낸스' 입력시 네이버 링크가 전송됩니다.
        '인베스팅' 입력시 네이버 링크가 전송됩니다.
        '유튜브' 입력시 네이버 링크가 전송됩니다. 
        8. 챗봇은 주식, 뉴스, 차트에 관한 내용에만 답변합니다. 질문시 주식,뉴스,차트에 관한 내용을 넣어주세요. 
        ex) 애플주식 차트 보여줘"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=helptext)

    # 메세지 보내는기능
    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        response = requests.post(url, params=params)
        return response.json()


    # 마지막 텍스트 가져오는 기능
    def message_text(self):
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
        database.update_user(chat_id, "Y")
        return chat_id

    def out_subscribe(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="구독 취소가 완료되었습니다.")
        database.update_user(chat_id, "N")
        return chat_id

    
    # 마지막 텍스트에 반응하는 기능
    def message_handler(update,context):
        msgtext = update.message.text
        chat_id = update.effective_chat.id
        user_data = context.user_data
        favorites_list = user_data.get('favorites_list', [])
        selectbuttons = user_data.get('selectbuttons', [])
        deepl_translator = DeeplTranslator(True)
        livecrawler = LiveCrawler()
        
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
            if len(favorites_list) != 0:
                if msgtext in favorites_list:
                    reply_markups = None
                    favorite_idx = favorites_list.index(msgtext)
                    if favorite_idx < len(selectbuttons):
                        reply_markups = InlineKeyboardMarkup([selectbuttons[favorite_idx]])
                        update.message.reply_text(f'{msgtext}', reply_markup=reply_markups)
                else:
                    if "주식" in msgtext or "차트"in msgtext or "뉴스"in msgtext:
                        gptquery = f"{msgtext}in the sentence above Tell me keywords,\n\
                                    Change keywords with stock codes to stock codes in Keywords and mark all keywords\n\
                                    no explanation needed\n\
                                    Example:\n\
                                    Keywords: Amazon (AMZN), today's price, recent news.\n\
                                    stock Keywords: [AMZN]or\n\
                                    stock Keywords: [001122.ks]or\n\
                                    no Keywords: [N/A]"  
                        messages = [
                                    {"role": "system", "content": "You are a helpful assistant."},
                                    {"role": "user", "content": gptquery}
                                    ]
                        response = openai.ChatCompletion.create(
                                    model=model,
                                    messages=messages
                                    )
                        answer = response['choices'][0]['message']['content']
                        location = re.search(r'\[(.*?)\]', answer).group(1)
                        context.bot.send_message(chat_id=chat_id, text="대답까지 1~2분정도 소요됩니다.")
                        if "차트" in msgtext:          
                            stock = StockData(location)
                            stock.screenshot(location)
                            stocktext = stock.get_stock_info(location)
                            context.bot.send_message(chat_id=chat_id, text=f"{stocktext} \n ▼차트 자세히보기▼ \n https://finance.yahoo.com/chart/{location}?showOptin=1")
                            with open(f'C:/Users/smhrd/stockimg/{location}.png','rb') as img:
                                context.bot.send_photo(chat_id = chat_id, photo = img)
                        elif "뉴스" in msgtext:
                            location = location.split(".")[0]
                            print("주식종목코드에서 .ks제거")
                            news = livecrawler.investing_search(location)
                            print("관련뉴스 링크 가져오기 완")
                            newstext = livecrawler.investing_crawl_page(news)
                            print("뉴스텍스트 가져오기 완")
                            news_summaries = summarize(newstext)
                            print("뉴스텍스트 요약 완")
                            translated_text = deepl_translator.translate(news_summaries)
                            print("뉴스 텍스트 번역")
                            context.bot.send_message(chat_id=chat_id, text=translated_text)
                    else:
                        context.bot.send_message(chat_id=chat_id, text="무슨 말인지 모르겠어요")
            else:
                if "주식" in msgtext or "차트"in msgtext or "뉴스"in msgtext:
                    gptquery = f"{msgtext}in the sentence above Tell me keywords,\n\
                                Change keywords with stock codes to stock codes in Keywords and mark all keywords\n\
                                no explanation needed\n\
                                Example:\n\
                                Keywords: Amazon (AMZN), today's price, recent news.\n\
                                stock Keywords: [AMZN]or\n\
                                stock Keywords: [001122.ks]or\n\
                                no Keywords: [N/A]"  
                    messages = [
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": gptquery}
                                ]
                    response = openai.ChatCompletion.create(
                                model=model,
                                messages=messages
                                )
                    answer = response['choices'][0]['message']['content']
                    location = re.search(r'\[(.*?)\]', answer).group(1)
                    context.bot.send_message(chat_id=chat_id, text="대답까지 1~2분정도 소요됩니다.")
                    if "차트" in msgtext:          
                        stock = StockData(location)
                        stock.screenshot(location)
                        stocktext = stock.get_stock_info(location)
                        context.bot.send_message(chat_id=chat_id, text=f"{stocktext} \n ▼차트 자세히보기▼ \n https://finance.yahoo.com/chart/{location}?showOptin=1")
                        with open(f'C:/Users/smhrd/stockimg/{location}.png','rb') as img:
                            context.bot.send_photo(chat_id = chat_id, photo = img)
                    elif "뉴스" in msgtext:
                        location = location.split(".")[0]
                        print("주식종목코드에서 .ks제거")
                        news = livecrawler.investing_search(location)
                        print("관련뉴스 링크 가져오기 완")
                        newstext = livecrawler.investing_crawl_page(news)
                        print("뉴스텍스트 가져오기 완")
                        news_summaries = summarize(newstext)
                        print("뉴스텍스트 요약 완")
                        translated_text = deepl_translator.translate(news_summaries)
                        print("뉴스 텍스트 번역")
                        context.bot.send_message(chat_id=chat_id, text=translated_text)
                    else:
                        context.bot.send_message(chat_id=chat_id, text="무슨 말인지 모르겠어요")    
                else:
                    context.bot.send_message(chat_id=chat_id, text="무슨 말인지 모르겠어요")
            
                    
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
        deepl_translator = DeeplTranslator(True)
        livecrawler = LiveCrawler()

        for favorite in favorites_list:
            if query_data == f'stock_{favorite}':
                context.bot.send_message(chat_id=query.message.chat_id, text="대답까지 1~2분정도 소요됩니다.")
                gptquery = f"{favorite}주식 뉴스 알려줘 in the sentence above Tell me keywords,\n\
                                Change keywords with stock codes to stock codes in Keywords and mark all keywords\n\
                                no explanation needed\n\
                                Example:\n\
                                Keywords: Amazon (AMZN), today's price, recent news.\n\
                                stock Keywords: [AMZN]or\n\
                                stock Keywords: [001122.ks]or\n\
                                no Keywords: [N/A]"  
                messages = [
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": gptquery}
                                ]
                response = openai.ChatCompletion.create(
                                model=model,
                                messages=messages
                                )
                answer = response['choices'][0]['message']['content']
                location = re.search(r'\[(.*?)\]', answer).group(1)
                location = location.split(".")[0]
                print("주식종목코드에서 .ks제거")
                news = livecrawler.investing_search(location)
                print("관련뉴스 링크 가져오기 완")
                newstext = livecrawler.investing_crawl_page(news)
                print("뉴스텍스트 가져오기 완")
                news_summaries = summarize(newstext)
                print("뉴스텍스트 요약 완")
                translated_text = deepl_translator.translate(news_summaries)
                print("뉴스 텍스트 번역")
                context.bot.send_message(chat_id=query.message.chat_id,
                                                    text=f"{favorite}주식 \n\{translated_text}")


            elif query_data == f'index_{favorite}':
                gptquery = f"{favorite}주식 차트 알려줘 in the sentence above Tell me keywords,\n\
                                Change keywords with stock codes to stock codes in Keywords and mark all keywords\n\
                                no explanation needed\n\
                                Example:\n\
                                Keywords: Amazon (AMZN), today's price, recent news.\n\
                                stock Keywords: [AMZN]or\n\
                                stock Keywords: [001122.ks]or\n\
                                no Keywords: [N/A]"  
                messages = [
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": gptquery}
                                ]
                response = openai.ChatCompletion.create(
                                model=model,
                                messages=messages
                                )
                answer = response['choices'][0]['message']['content']
                location = re.search(r'\[(.*?)\]', answer).group(1)
                context.bot.send_message(chat_id=query.message.chat_id, text="대답까지 1~2분정도 소요됩니다.")
                stock = StockData(location)
                stock.screenshot(location)
                stocktext = stock.get_stock_info(location)
                context.bot.send_message(chat_id=query.message.chat_id, text=f"{stocktext} \n ▼차트 자세히보기▼ \n https://finance.yahoo.com/chart/{location}?showOptin=1")
                with open(f'C:/Users/smhrd/stockimg/{location}.png','rb') as img:
                    context.bot.send_photo(chat_id = query.message.chat_id, photo = img)
                
