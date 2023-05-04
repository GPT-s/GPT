from src.database import DataBase
from src.crawler import InvestingCrawler
from src.translator_deepl import DeeplTranslator
from src.telegram_handler import TelegramHandler
from src.gpt import GPT
import schedule
import time
from datetime import datetime
import sentry_sdk
import logging
from dotenv import load_dotenv
import os

load_dotenv()
DSN = os.environ.get("DSN")

dsn = DSN

sentry_sdk.init(
    dsn=DSN,
)

# logging
# format : 형식
# %(asctime)s : 기록된 시간
# %(levelname)s : 로그 메시지 레벨
# %(message)s : 로그 메시지
# level : 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# DEBUG: 가장 상세한 정보를 제공. 일반적으로 문제 해결에 사용. 이는 일반적으로 모든 로그 메시지를 포함하며, 로그 시스템이 제대로 작동하고 있는지 확인하는 데 사용.
# INFO: 일반적으로 애플리케이션이 제대로 작동하고 있음을 확인하는 데 사용. 예를 들어, 서버가 시작되었거나 중단되었음을 알릴 때 사용.
# WARNING: 예상치 못한 일이 발생했거나, 문제가 발생할 수 있는 상황이 가까워졌음을 나타냄. 하지만 소프트웨어는 여전히 제대로 작동.
# ERROR: 더 심각한 문제가 발생했음을 나타냄. 소프트웨어가 일부 기능을 수행하지 못하게 되었을 가능성이 있음.
# CRITICAL: 가장 심각한 에러를 의미. 프로그램 자체가 계속 실행할 수 없을 수 있음.

# logging.INFO :  INFO, WARNING, ERROR, CRITICAL 레벨의 메시지만 로깅 (INFO 레벨 이상만)

logging.basicConfig(filename="main.log", format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


class Pipeline:
    def __init__(self):
        try:
            self.gpt = GPT()
            self.database = DataBase()
            self.crawler = InvestingCrawler()
            self.telegram_handler = TelegramHandler()
            # 오류를 강제로 발생
            # raise ValueError("파이프라인 초기화 강제 오류")
        except Exception as e:
            logging.error(f"Init error: {e}")
            # sentry.io 추가하기
            sentry_sdk.capture_exception(e)

    def run(self):
        # 1. 링크 크롤링
        latest_links = self.crawler.get_latest_links()
        
        # 2. 크롤링한 링크를 데이터 베이스에 저장
        current_datetime = datetime.now()
        for link in latest_links:
            self.database.insert_link(link, current_datetime)
        
        # 3. 데이터 베이스에서 저장한 링크를 꺼내온다
        news_to_update = self.database.select_news()
        
        for news in news_to_update:
            news_id, source, _, _, _, _ = news
            
            # 4. 링크로 들어가서 뉴스 텍스트를 크롤링 해온다
            text = self.crawler.crawl_page(source)
            
            # 5. 크롤링한 뉴스를 감성분석하고 요약한다
            sentiment_and_summary = self.gpt.summarize_news(text)


            # 감정과 요약은 단일 문자열로 반환되므로 이를 분할해야 합니다.
            sentiment, summary_list = sentiment_and_summary
            summary = ' '.join(summary_list)

            
            # 6. 감성분석을 데이터베이스에 업데이트한다
            self.database.update_news_sentiment(news_id, sentiment)
            self.translator = DeeplTranslator()
            # 7. 요약한 뉴스를 번역한다
            translated_summary = self.translator.translate(summary)
            
            # 8. 번역한 뉴스를 데이터베이스에 업데이트한다
            self.database.update_news_summary(news_id, translated_summary)


    def sent_message(self):
        try:
            print("뉴스 보내기 222222222")
            print("뉴스 보내기 222222222")
            print("뉴스 보내기 222222222")
            news_list = self.database.select_news()

            for news in news_list:
                if not news[4]:
                    message = f"Source: {news[1]}\nSummary: {news[2]}\nDatetime: {news[3]}"
                    telegram_chat_id = '5292915370'
                    self.telegram_handler.send_message(telegram_chat_id, message)
                    self.database.update_news_sent(news[0])
        except Exception as e:
            print(f"Sent message error: {e}")
            logging.error(f"Sent message error: {e}")
            # sentry.io 추가하기
            sentry_sdk.capture_exception(e)
            


try:
    pipeline = Pipeline()
    pipeline.run()
    pipeline.sent_message()

    # schedule.every().day.at("12:18").do(pipeline.crawling)
    # schedule.every().day.at("12:20").do(pipeline.sent_message)
    schedule.every(5).minutes.do(pipeline.crawling)

    # 스케줄 실행
    while True:
        # 설정된 스케줄에 따라 예약된 모든 작업을 실행
        schedule.run_pending()
        # 1초동안 멈추게 해서 while문 과부하를 방지
        time.sleep(1)
except Exception as e:
    print(f"Main error: {e}")
    logging.error(f"Main error: {e}")
    # sentry.io 추가하기
    sentry_sdk.capture_exception(e)