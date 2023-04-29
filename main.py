from src.database import DataBase
from src.crawler import InvestingCrawler
from src.translator_deepl import DeeplTranslator
from src.telegram_handler import TelegramHandler
import schedule
import time

class Pipeline:
    def __init__(self):
        try:
            print("init")
            print("init")
            print("init")
            self.database = DataBase()
            self.crawler = InvestingCrawler()
            self.translator = DeeplTranslator()
            self.telegram_handler = TelegramHandler()
        except Exception as e:
            print(f"Init error: {e}")
            # sentry.io 추가하기


    def crawling(self):
        try:
            self.crawler = InvestingCrawler()
            self.translator = DeeplTranslator()
            print("메인 크롤링111111")
            print("메인 크롤링111111")
            print("메인 크롤링111111")
            self.crawler.investing_latest()
        except Exception as e:
            print(f"Crawling error: {e}")
            # sentry.io 추가하기

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
            # sentry.io 추가하기
            


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
    # sentry.io 추가하기
