import src.crawler  
from src.finbert import bert 
from src.gpt import get_completion, summarize, get_summary_list
from src.gpt_sent import sentiment_analysis
import src.stock_idx  
from src.telegram_handler import start, help, send_message, message_text, favorites, message_handler, remove_favorite, on_callback_query, main
from src.crawler import investing_latest_news

investing_latest_news = src.crawler.investing_latest_news()


#print(investing_search)

for text in investing_latest_news:
    finbert = bert
    result_bert = finbert(text) # 핀버트 감성 분석 변수 선언
    gpt = summarize
    result_gpt = summarize(text) # 지피티 요약 변수 선언
    print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
    print(result_gpt)
    telegram_send_message = send_message("5999372705", text =f"{result_gpt}\n{text}\n{result_bert}")
    telegram_send_message




