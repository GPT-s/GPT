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

import asyncio
load_dotenv()
DSN = os.environ.get("DSN")

dsn = DSN

sentry_sdk.init(
    dsn=DSN,
)


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
            print(f"Init error: {e}")
            logging.error(f"Init error: {e}")
            # sentry.io 추가하기
            sentry_sdk.capture_exception(e)

    async def crawling (self):
        # 1. 링크 크롤링
        latest_links = await self.crawler.get_latest_links()
        
        # 2. 크롤링한 링크를 데이터 베이스에 저장
        current_datetime = datetime.now()
        for link in latest_links:
            self.database.insert_link(link, current_datetime)
        
        # 3. 데이터 베이스에서 저장한 링크를 꺼내온다
        news_to_update = self.database.select_news()
        
        for news in news_to_update:
            news_id, source, _, _, _, _ = news
            
            # 4. 링크로 들어가서 뉴스 텍스트를 크롤링 해온다
            text = await self.crawler.crawl_page(source)
            
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
            print("뉴스 보내기어쩔")
            print("뉴스 보내기")
            print("뉴스 보내기")
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
    asyncio.run(pipeline.crawling())
    # pipeline.sent_message()

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