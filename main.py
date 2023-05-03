from src.database import DataBase
from src.crawler import InvestingCrawler
from src.translator_deepl import DeeplTranslator
from src.telegram_handler import TelegramHandler
import schedule
import time
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
            print("init")
            print("init")
            print("init")
            self.database = DataBase()
            self.crawler = InvestingCrawler()
            self.telegram_handler = TelegramHandler()
            # 오류를 강제로 발생
            # raise ValueError("파이프라인 초기화 강제 오류")
        except Exception as e:
            print(f"Init error: {e}")
            logging.error(f"Init error: {e}")
            # sentry.io 추가하기
            sentry_sdk.capture_exception(e)


    def crawling(self):
        try:
            self.crawler = InvestingCrawler()
            print("메인 크롤링111111")
            print("메인 크롤링111111")
            print("메인 크롤링111111")
            self.crawler.investing_latest()
        except Exception as e:
            print(f"Crawling error: {e}")
            logging.error(f"Crawling error in the main: {e}")
            # sentry.io 추가하기
            sentry_sdk.capture_exception(e)

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
    pipeline.crawling()
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