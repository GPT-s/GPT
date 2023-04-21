from src.crawler import Investing_Crawler
from src.finbert import FinBert
from src.gpt import summarize
#import src.gpt_sent
#import src.stock_idx  
from src.telegram_handler import TelegramHandler
from src.gpt_keyword import get_analyze_keyword, analyze_keyword
from test.test_db import db

investing_latest_news = Investing_Crawler()
Finbert = FinBert()
send_message = TelegramHandler()

for text in investing_latest_news: # 모듈 통합 실행 코드 
    result_sentiment = Finbert.sentiment(text)# 핀버트 감성 분석 변수
    result_gpt = summarize(text) # 지피티 요약 변수
    print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
    translator = translator_deepl(result_gpt)
    telegram_send_message = send_message("5999372705", text =f"**요약된 뉴스**\n{translator}\n\n'**감성 분석**'\n\n{result_sentiment}\n\n**뉴스 링크**\n\n{text}") # 해당 아이디의 텔레그램에 내용 전송
    telegram_send_message