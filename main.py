import time
import schedule
from datetime import datetime
from src.finbert import FinBert
from src.gpt import summarize, get_summary_list
from src.crawler import InvestingCrawler
from src.database import DataBase
from src.telegram_handler import TelegramHandler
from src.translator_deepl import DeeplTranslator

# pip install schedule
import schedule


# 클래스 가져 오는 거
investing_crawler = InvestingCrawler()
finbert = FinBert()
database = DataBase()
telegram_handler = TelegramHandler()
deepl_translator = DeeplTranslator(True)

# 최신 뉴스 가져오기 및 감성 분석 및 뉴스 요약
def get_latest_news():
    
    # 최신뉴스와 텍스트를 가져와서 변수에 담아줌
    latest_links, latest_texts = investing_crawler.investing_latest()
    
    # 뉴스 텍스트를 감성 분석하고 결과를 변수에 담아줌
    sentiment_data = finbert.sentiment(latest_texts)
    
    # 감성 분석 결과를 바탕으로 요약함
    summaries = get_summary_list(sentiment_data['data'])
    
    # 최신 뉴스의 링크, 텍스트, 요약을 반환함
    return latest_links, latest_texts, summaries

def process_and_send_news():
    # 메시지 보낼때 링크랑 내용 안맞는데 수정해야 함
    # 뭐가 문제지 과거에도 같은 링크를 사용하나?
    print("1. 크롤링 및 감성 분석 시작")
    print("1. 크롤링 및 감성 분석 시작")
    print("1. 크롤링 및 감성 분석 시작")
    print("1. 크롤링 및 감성 분석 시작")
    print("1. 크롤링 및 감성 분석 시작")
    
    # 위 함수에서 반환한 값을 호출해서 변수에 담아줌
    # get_latest_news()의 반환값이 3개이고 순서대로 변수에 할당 됨
    latest_links, latest_texts, summaries = get_latest_news()

    # 요약된 뉴스와 함께 데이터베이스에 저장
    print("2. 데이터베이스 저장 시작")
    print("2. 데이터베이스 저장 시작")
    print("2. 데이터베이스 저장 시작")
    print("2. 데이터베이스 저장 시작")
    print("2. 데이터베이스 저장 시작")

    
    # for문을 사용해서 링크, 텍스트, 요약을 데이터 베이스에 저장함
    # datetime.now()를 사용해서 현재 시간도 함께 저장함
    # 여러개의 리스트에서 동일한 인덱스에 있는 항목을 튜플로 묶어줌 
    # latest_links, latest_texts, summaries 3개의 리스트가 있는데
    # 이 리스트의 동일한 인덱스에 있는 항목을 묶어 튜플(link, text, summary)로 만들어 줌
    for link, text, summary in zip(latest_links, latest_texts, summaries):
        # 요약전 텍스트는 필요없어서 ""로 저장
        database.insert_news(link, "", summary, datetime.now())
    
def send_translated_news():
   
    # 데이터베이스에서 뉴스 선택
    print("3. 번역 및 텔레그램 전송 시작")
    print("3. 번역 및 텔레그램 전송 시작")
    print("3. 번역 및 텔레그램 전송 시작")
    print("3. 번역 및 텔레그램 전송 시작")
    print("3. 번역 및 텔레그램 전송 시작")
   
    # 데이터베이스에서 뉴스를 선택함
    news_list = database.select_ho_news()

    # 선택된 뉴스를 번역하고 텔레그램으로 전송
    
    # for문을 사용해서 선택된 뉴스를 번역하고, 텔레그램으로 전송
    for news in news_list:
        
        # sent 상태가 FALSE인 경우에만 뉴스를 처리합니다.(전송되지 않은 뉴스만 처리) 
        if not news[5]:  # news[5]는 DB 테이블 6번째에 있는 컬럼
            
            # news[0] : 뉴스id(자동 인덱스), 
            # news[1] : 뉴스 링크
            # news[2] : 뉴스 텍스트
            # news[3] : 뉴스 요약
            # news[4] : 뉴스 작성 날짜
            # news[5] : 뉴스 전송 여부
            
            # 요약된 뉴스를 호출해서 번역 함수로 번역
            translated_text = deepl_translator.translate(news[3])
            
            # 번역된 뉴스와 링크를 출력 양식?으로 만들고 변수에 저장
            message = f"**요약된 뉴스**\n{translated_text}\n\n원문 링크: {news[1]}"

            # 여기는 유저 아이디 변수로 넣어주면 될 듯
            telegram_chat_id = '5292915370'

            # 텔레그램 메시지 전송을 변수로 만들어줌
            # 굳이 안만들어줘도 됨. 
            # 나중에 다른 곳에서 쓸 수도 있으니까 혹시 몰라서
            telegram_send_message = telegram_handler.send_message(telegram_chat_id, text=message)

            # 해당 아이디의 텔레그램에 내용 전송 실행
            telegram_send_message

            # 뉴스를 전송한 후에 데이터베이스에 전송 여부를 업데이트합니다.
            database.update_news_sent(news[0])  # news[0]는 DB 테이블 1번째에 있는 컬럼

    print("작업 완")


# 스케줄러 설정
# 크롤링 하는 함수를 5분 마다 실행
# 반복 하는거 테스트 좀 해봐야 할 듯 처음 실행은 되는데 두번째에 안되는건가
schedule.every(5).minutes.do(process_and_send_news)

# 테스트 해보려면 여기 아래 시간을 바꾸세여. 지금시간에 1~2분 더해서 그러면 크롤링하고 저장함
schedule.every().day.at("19:14").do(process_and_send_news)

# 번역 후 메시지 보내는 함수를 08:30 마다 실행 
schedule.every().day.at("08:30").do(send_translated_news)

# 테스트 해보려면 여기 아래 시간을 바꾸세여. 위에 크롤링 작동 시간에 2분 더해서 그러면 저장한거 메시지 보냄
schedule.every().day.at("19:20").do(send_translated_news)

# 스케줄 실행
while True:
    # 설정된 스케줄에 따라 예약된 모든 작업을 실행
    schedule.run_pending()
    # 1초동안 멈추게 해서 while문 과부하를 방지
    time.sleep(1)


# 원래 있던 부분
# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼

# from src.crawler import InvestingCrawler
# import src.crawler
# from src.finbert import FinBert
# from src.gpt import summarize
# #import src.gpt_sent
# #import src.stock_idx  
# from src.telegram_handler import TelegramHandler
# from src.gpt_keyword import get_analyze_keyword, analyze_keyword
# from src.database import DataBase
# import os

# investing_latest_news = InvestingCrawler()
# finbert = FinBert()

# translate = src.crawler # 크롤러 모듈 내부 번역기 사용 전용 변수
# teltoken = os.environ.get('teltoken')
# token = teltoken
# send_message = TelegramHandler(token)


# class Main:

#         if send_message.start('/start'): # 사용자가 챗봇 생성 시 실행
#                insert_data_user = DataBase().insert_user('5611753679','F')
#                insert_data_user
#                send_message.send_message('5611753679', '아이디 생성 완료')
#                  #실행 됨.

#         elif send_message.equals('/sub'): # 사용자가 sub 명령어 입력 시 실행
#                 update_data_sub = DataBase().update_user('5611753679', 'T')
#                 update_data_sub
#                 #send_message.send_message('5999372705', '구독하기')

#         elif send_message.equals('/nosub'): # 사용자가 nosub 명령어 입력 시 실행
#                 update_data_nosub = DataBase().update_user('5611753679', 'F')
#                 update_data_nosub
#                 #send_message.send_message('5999372705', '구독취소')

#         elif send_message.message_handler() != '/nosub'&'/sub'&'/start': # 사용자가 뉴스 데이터 요청 시 실행

#              for text in investing_latest_news: # 사용자 요청 시 실행하는 부분
#                      result_sentiment = finbert.sentiment(text)# 핀버트 감성 분석 변수
#                      result_gpt = summarize(text) # 지피티 요약 변수
#                      print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
#                      translator = translate.deepL_Translator(result_gpt)
#                      telegram_send_message = send_message.send_message('5611753679', text =f"**요약된 뉴스**\n{translator}\n\n**뉴스 링크**\n\n{text}") # 해당 아이디의 텔레그램에 내용 전송
#                      telegram_send_message
  
               
            













# #insert_data_user = DataBase().insert_user('5999372705','F')
# #update_data_sub = DataBase().update_user('5999372705', 'T')
# #update_data_nosub = DataBase().update_user('5999372705', 'F')






# class Main:

#         if send_message.telegram_main().equals('/start'): # 사용자가 챗봇 생성 시 실행
#                 insert_data_user = DataBase().insert_user('5611753679','F')
#                 insert_data_user
#                 send_message.send_message('5611753679', '아이디 생성 완료')
#                 #실행 됨.

#         elif send_message.telegram_main().equals('/sub'): # 사용자가 sub 명령어 입력 시 실행
#                 update_data_sub = DataBase().update_user('5611753679', 'T')
#                 update_data_sub
#                     #send_message.send_message('5999372705', '구독하기')

#         # elif send_message.telegram_main().equals('/nosub'): # 사용자가 nosub 명령어 입력 시 실행
#         #         update_data_nosub = DataBase().update_user('5611753679', 'F')
#         #         update_data_nosub
#                     #send_message.send_message('5999372705', '구독취소')

#         elif send_message.send_message().equals(send_message.message_handler): # 사용자가 뉴스 데이터 요청 시 실행

#             for text in investing_latest_news: # 사용자 요청 시 실행하는 부분
#                     result_sentiment = finbert.sentiment(text)# 핀버트 감성 분석 변수
#                     result_gpt = summarize(text) # 지피티 요약 변수
#                     print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
#                     translator = translate.deepL_Translator(result_gpt)
#                     telegram_send_message = send_message.send_message('5611753679', text =f"**요약된 뉴스**\n{translator}\n\n**뉴스 링크**\n\n{text}") # 해당 아이디의 텔레그램에 내용 전송
#                     telegram_send_message
#         #if send_message.telegram_main().equals('/종료'):
#         #   print('챗봇을 종료합니다.')
            

