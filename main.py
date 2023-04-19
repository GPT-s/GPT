import src.crawler  
from src.finbert import bert 
from src.gpt import summarize
#import src.gpt_sent
#import src.stock_idx  
from src.telegram_handler import send_message
from src.crawler import investing_latest_news

investing_latest_news = src.crawler.investing_latest_news()

for text in investing_latest_news: # 모듈 통합 실행 코드 
    finbert = bert
    result_bert = finbert(text) # 핀버트 감성 분석 변수
    gpt = summarize
    result_gpt = summarize(text) # 지피티 요약 변수
    print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
    print(result_gpt)
    telegram_send_message = send_message("5999372705", text =f"{result_gpt}\n{text}\n{result_bert}") # 해당 아이디의 텔레그램에 내용 전송
    telegram_send_message