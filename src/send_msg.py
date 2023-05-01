from database import DataBase
from telegram_handler import TelegramHandler
import sentry_sdk
import logging

def sent_message():
    try:
        database = DataBase()
        telegram_handler = TelegramHandler()
        print("뉴스 보내기 222222222")
        print("뉴스 보내기 222222222")
        print("뉴스 보내기 222222222")
        news_list = database.select_news()

        for news in news_list:
            if not news[4]:
                message = f"Source: {news[1]}\nSummary: {news[2]}\nDatetime: {news[3]}"
                telegram_chat_id = '5292915370'
                telegram_handler.send_message(telegram_chat_id, message)
                database.update_news_sent(news[0])
    except Exception as e:
        print(f"Sent message error: {e}")
        logging.error(f"Sent message error: {e}")
        # sentry.io 추가하기
        sentry_sdk.capture_exception(e)

sent_message()