import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telepot.namedtuple import InlineKeyboardMarkup as MU 
from telepot.namedtuple import InlineKeyboardButton as BT 
from telegram import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup
import openai
from dotenv import load_dotenv
import os
from src.database import DataBase
import re
from src.stock_idx import StockData
from src.translator_deepl import DeeplTranslator
from src.livecrawler import LiveCrawler
from src.gpt import summarize,keyword

load_dotenv()

teltoken = os.environ.get('teltoken')
token = teltoken

GPTAPI = os.environ.get('GPTAPI')
OPENAI_API_KEY = GPTAPI
openai.api_key = OPENAI_API_KEY
database = DataBase()




class TelegramHandler:
    
    def __init__(self):
        self.token = token
        self.updater = Updater(token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', TelegramHandler.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', TelegramHandler.help))
        self.updater.dispatcher.add_handler(CommandHandler('sub', TelegramHandler.in_subscribe))
        self.updater.dispatcher.add_handler(CommandHandler('unsub', TelegramHandler.out_subscribe))
        self.updater.dispatcher.add_handler(CommandHandler('fav', TelegramHandler.favorites, pass_user_data=True))
        self.updater.dispatcher.add_handler(CommandHandler('del', TelegramHandler.remove_favorite, pass_user_data=True))
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
        helptext = """🔔챗봇 사용 설명서🔔──────────
        1️⃣ [  /fav 주식이름  ]으로 키보드버튼을 추가할 수 있습니다.

        2️⃣ [  /del 주식이름  ]으로 키보드 버튼을 삭제할 수 있습니다.

        3️⃣ 키보드 버튼 클릭시 해당 버튼에 대한 뉴스 / 차트 버튼 
                 메세지가 전송됩니다.
        4️⃣ 뉴스 또는 차트 버튼 클릭시 버튼에 해당하는 내용의 메세지가 
                 전송됩니다.
        5️⃣ [  /sub  ] 커맨드입력으로 8시30분 15시30분에 발송되는 
                 주식뉴스를 구독할 수 있습니다.
        6️⃣ [  /unsub  ] 커맨드입력으로 8시30분 15시30분에 발송되는 
                 주식뉴스를 구독 취소할 수 있습니다.
        7️⃣ 특정사이트 링크
                 1. '네이버' 입력시 네이버 링크가 전송됩니다.
                 2. '구글' 입력시 네이버 링크가 전송됩니다.
                 3. '야후파이낸스' 입력시 네이버 링크가 전송됩니다.
                 4. '인베스팅' 입력시 네이버 링크가 전송됩니다.
                 5. '유튜브' 입력시 네이버 링크가 전송됩니다. 
        8️⃣ 챗봇은 주식, 뉴스, 차트에 관한 내용에만 답변합니다. 
                 질문시 주식,뉴스,차트에 관한 내용을 넣어주세요. 
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
        if not message_text.lower().startswith('/fav '):
            return
        search_query = message_text.lower().replace('/fav ', '')
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
                        stockcode = keyword(msgtext)
                        print(f"{stockcode}생성완료")
                        context.bot.send_message(chat_id=chat_id, text="대답까지 1~2분정도 소요됩니다.")
                        if "차트" in msgtext:          
                            stock = StockData(stockcode)
                            stock.screenshot(stockcode)
                            stocktext = stock.get_stock_info(stockcode)
                            context.bot.send_message(chat_id=chat_id, text=f"{stocktext} \n ▼차트 자세히보기▼ \n https://finance.yahoo.com/chart/{stockcode}?showOptin=1")
                            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                            folder_path = os.path.join(desktop_path, "stockimg")
                            with open(os.path.join(folder_path, f"{stockcode}.png"),"rb") as img:
                                context.bot.send_photo(chat_id = chat_id, photo = img)
                                img.close()
                                os.remove(os.path.join(folder_path,f"{stockcode}.png"))
                                print("삭제완료")
                        elif "뉴스" in msgtext:
                            location = stockcode.split(".")[0]
                            print("주식종목코드에서 .ks제거")
                            news = livecrawler.investing_search(location)
                            print("관련뉴스 링크 가져오기 완")
                            newstext = livecrawler.investing_crawl_page(news)
                            print("뉴스텍스트 가져오기 완")
                            sentiment_answer, summarize_answer = summarize(newstext)
                            print("뉴스텍스트 요약 완")
                            translated_text = deepl_translator.translate(summarize_answer)
                            print("뉴스 텍스트 번역")
                            context.bot.send_message(chat_id=chat_id, text=f"▼요약▼ \n 감성분석 : {sentiment_answer} \n {translated_text} \n\n 링크 : {news}")
                    else:
                        context.bot.send_message(chat_id=chat_id, text="무슨 말인지 모르겠어요")
            else:
                if "주식" in msgtext or "차트"in msgtext or "뉴스"in msgtext:
                    stockcode = keyword(msgtext)
                    print(f"{stockcode}생성완료")
                    context.bot.send_message(chat_id=chat_id, text="대답까지 1~2분정도 소요됩니다.")
                    if "차트" in msgtext:          
                        stock = StockData(stockcode)
                        stock.screenshot(stockcode)
                        stocktext = stock.get_stock_info(stockcode)
                        context.bot.send_message(chat_id=chat_id, text=f"{stocktext} \n ▼차트 자세히보기▼ \n https://finance.yahoo.com/chart/{stockcode}?showOptin=1")
                        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                        folder_path = os.path.join(desktop_path, "stockimg")
                        with open(os.path.join(folder_path, f"{stockcode}.png"),"rb") as img:
                            context.bot.send_photo(chat_id = chat_id, photo = img)
                            img.close()
                            os.remove(os.path.join(folder_path,f"{stockcode}.png"))
                            print("삭제완료")
                    elif "뉴스" in msgtext:
                        location = stockcode.split(".")[0]
                        print("주식종목코드에서 .ks제거")
                        news = livecrawler.investing_search(location)
                        print("관련뉴스 링크 가져오기 완")
                        newstext = livecrawler.investing_crawl_page(news)
                        print("뉴스텍스트 가져오기 완")
                        sentiment_answer, summarize_answer = summarize(newstext)
                        print("뉴스텍스트 요약 완")
                        translated_text = deepl_translator.translate(summarize_answer)
                        print("뉴스 텍스트 번역")
                        context.bot.send_message(chat_id=chat_id, text=f"▼요약▼ \n 감성분석 : {sentiment_answer} \n {translated_text} \n\n 링크 : {news}")
                    else:
                        context.bot.send_message(chat_id=chat_id, text="무슨 말인지 모르겠어요")    
                else:
                    context.bot.send_message(chat_id=chat_id, text="무슨 말인지 모르겠어요")
            
                    
    # 즐겨찾기 삭제하는 커맨드  /remove 삭제할종목
    def remove_favorite(update, context):
        message_text = update.message.text
        if not message_text.lower().startswith('/del '):
            return
        remove_query = message_text.lower().replace('/del ', '')
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
                stockcode = keyword(f"{favorite}주식 뉴스 알려줘")
                print(f"{stockcode}생성완료")
                context.bot.send_message(chat_id=query.message.chat_id, text="대답까지 1~2분정도 소요됩니다.")
                location = stockcode.split(".")[0]
                print("주식종목코드에서 .ks제거")
                news = livecrawler.investing_search(location)
                print("관련뉴스 링크 가져오기 완")
                newstext = livecrawler.investing_crawl_page(news)
                print("뉴스텍스트 가져오기 완")
                sentiment_answer, summarize_answer = summarize(newstext)
                print("뉴스텍스트 요약 완")
                translated_text = deepl_translator.translate(summarize_answer)
                print("뉴스 텍스트 번역")
                context.bot.send_message(chat_id=query.message.chat_id, text=f"{favorite}주식 \n ▼요약▼ \n 감성분석 : {sentiment_answer} \n {translated_text} \n\n 링크 : {news}")

            elif query_data == f'index_{favorite}':
                stockcode = keyword(f"{favorite}주식 차트 알려줘")
                context.bot.send_message(chat_id=query.message.chat_id, text="대답까지 1~2분정도 소요됩니다.")
                stock = StockData(stockcode)
                stock.screenshot(stockcode)
                stocktext = stock.get_stock_info(stockcode)
                context.bot.send_message(chat_id=query.message.chat_id, text=f"{stocktext} \n ▼차트 자세히보기▼ \n https://finance.yahoo.com/chart/{stockcode}?showOptin=1")
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                folder_path = os.path.join(desktop_path, "stockimg")
                with open(os.path.join(folder_path, f"{stockcode}.png"),"rb") as img:
                    context.bot.send_photo(chat_id = query.message.chat_id, photo = img)
                    img.close()
                    os.remove(os.path.join(folder_path,f"{stockcode}.png"))
                    print("삭제완료")
