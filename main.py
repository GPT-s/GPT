import time
from datetime import datetime
from src.finbert import FinBert
from src.gpt import summarize, get_summary_list
from src.crawler import InvestingCrawler
from src.database import DataBase
from src.telegram_handler import TelegramHandler
from src.translator_deepl import DeeplTranslator

# pip install schedule
import schedule


# 코드 길어 보여도 다 주석이랑 print 임
# GPT-api 크레딧 많이 먹어서 크롤링 3개씩만 함

class Pipeline():
    def __init__(self):
        self.investing_crawler = InvestingCrawler()
        # self.finbert = FinBert()
        self.database = DataBase()
        self.deepl_translator = DeeplTranslator(True)
        self.telegram_handler = TelegramHandler()

    def get_latest_news(self):
        self.investing_crawler = InvestingCrawler()
    
        latest_links, latest_texts = self.investing_crawler.investing_latest()
        
        # 뉴스 텍스트를 감성 분석하고 결과를 변수에 담아줌
        # sentiment_data = self.finbert.sentiment(latest_texts)

        # 감성 분석 결과를 바탕으로 요약함
        summaries = get_summary_list(latest_texts)

        # 최신 뉴스의 링크, 텍스트, 요약을 반환함
        return latest_links, latest_texts, summaries
    
    def process_and_send_news(self):
    
        # 시간 측정 그냥 얼마나 걸리나 궁금해서
        start_time = time.time()

        # 메시지 보낼때 링크랑 내용 안맞는데 수정해야 함
        # 뭐가 문제지 과거에도 같은 링크를 사용하나?
        # 언제는 맞고 언제는 틀리고 뭐징
        print("1. 크롤링 및 감성 분석 시작")
        print("1. 크롤링 및 감성 분석 시작")
        print("1. 크롤링 및 감성 분석 시작")
        print("1. 크롤링 및 감성 분석 시작")
        print("1. 크롤링 및 감성 분석 시작")
        
        # 위 함수에서 반환한 값을 호출해서 변수에 담아줌
        # get_latest_news()의 반환값이 3개이고 순서대로 변수에 할당 됨
        latest_links, latest_texts, summaries = self.get_latest_news()

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
            self.database.ho_insert_news(link, "", summary, datetime.now())
        
        # 시간 측정
        end_time = time.time()
        Total_time = end_time - start_time

        print(f"크롤링부터 저장까지 걸린 시간: {Total_time:.2f} 초")

    def send_translated_news(self):

        self.deepl_translator = DeeplTranslator(True)
        # 시간 측정 그냥 얼마나 걸리나 궁금해서    
        start_time = time.time()
    
    
        # 데이터베이스에서 뉴스 선택
        print("3. 번역 및 텔레그램 전송 시작")
        print("3. 번역 및 텔레그램 전송 시작")
        print("3. 번역 및 텔레그램 전송 시작")
        print("3. 번역 및 텔레그램 전송 시작")
        print("3. 번역 및 텔레그램 전송 시작")
    
        # 데이터베이스에서 뉴스를 선택함
        news_list = self.database.select_ho_news()

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
                translated_text = self.deepl_translator.translate(news[3])
                
                # 번역된 뉴스와 링크를 출력 양식?으로 만들고 변수에 저장
                message = f"**요약된 뉴스**\n{translated_text}\n\n원문 링크: {news[1]}"

                # 유저아이디 전부 가져오기
                chat_id_list = self.database.select_user_id()
                
                # 모든 유저에게 메시지 보내기
                for chat_id in chat_id_list:
                    telegram_chat_id = chat_id[0]
                    self.telegram_handler.send_message(telegram_chat_id, text=message)

                self.database.update_news_sent(news[0])

        print("작업 완")
        end_time = time.time()
        Total_time = end_time - start_time

        print(f"저장된 뉴스 가져와서 메시지 보내기까지 걸린 시간: {Total_time:.2f} 초")
                
                # 본인한테만 메시지 보내기
                # 유저아이디 전부 가져오기 부터
                # 저장된 뉴스 시간 프린트까지 주석 처리하고
                # # 여기는 유저 아이디
                # telegram_chat_id = '5292915370'

                # # 텔레그램 메시지 전송을 변수로 만들어줌
                # # 굳이 안만들어줘도 됨. 
                # # 나중에 다른 곳에서 쓸 수도 있으니까 혹시 몰라서
                # telegram_send_message = self.telegram_handler.send_message(telegram_chat_id, text=message)

                # # 해당 아이디의 텔레그램에 내용 전송 실행
                # telegram_send_message

                # # 뉴스를 전송한 후에 데이터베이스에 전송 여부를 업데이트합니다.
                # self.database.update_news_sent(news[0])  # news[0]는 DB 테이블 1번째에 있는 컬럼

        # print("작업 완")
        # # 시간 측정
        # end_time = time.time()
        # Total_time = end_time - start_time

        # print(f"저장된 뉴스 가져와서 메시지 보내기까지 걸린 시간: {Total_time:.2f} 초")

pipeline = Pipeline()

# 스케줄러 설정

# 테스트 해보려면 여기 아래 시간을 바꾸세요. 지금 시간에 1~2분 더해서 그러면 크롤링하고 저장함
schedule.every().day.at("10:50").do(lambda: pipeline.process_and_send_news())

# 크롤링하는 함수를 5분 마다 실행
schedule.every(5).minutes.do(lambda: pipeline.process_and_send_news())

# 번역 후 메시지 보내는 함수를 08:30 마다 실행
schedule.every().day.at("08:30").do(lambda: pipeline.send_translated_news())

# 테스트 해보려면 여기 아래 시간을 바꾸세요. 위에 크롤링 작동 시간에 2분 더해서 그러면 저장한거 메시지 보냄
schedule.every().day.at("10:52").do(lambda: pipeline.send_translated_news())

# 스케줄 실행
while True:
    # 설정된 스케줄에 따라 예약된 모든 작업을 실행
    schedule.run_pending()
    # 1초동안 멈추게 해서 while문 과부하를 방지
    time.sleep(1)
