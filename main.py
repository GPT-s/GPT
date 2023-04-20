import src.crawler
from src.finbert import FinBert
from src.gpt import summarize

# import src.gpt_sent
# import src.stock_idx
from src.telegram_handler import send_message
from src.crawler import investing_latest_news, deepL_Translator
from src.gpt_keyword import get_analyze_keyword, analyze_keyword

investing_latest_news = src.crawler.investing_latest_news()
Finbert = FinBert()

# text_analyze = "엔비디아 가격 알려줘"
# Keyword_analyze = analyze_keyword(text_analyze)
# print(get_analyze_keyword(Keyword_analyze))


for text in investing_latest_news:  # 모듈 통합 실행 코드
    result_sentiment = Finbert.sentiment(text)
    # 핀버트 감성 분석 변수
    gpt = summarize
    result_gpt = summarize(text)  # 지피티 요약 변수
    print(
        "─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"
    )
    translator = deepL_Translator(result_gpt)
    telegram_send_message = send_message(
        "5999372705",
        text=f"**요약된 뉴스**\n{translator}\n\n'**감성 분석**'\n\n{result_sentiment}\n\n**뉴스 링크**\n\n{text}",
    )  # 해당 아이디의 텔레그램에 내용 전송
    telegram_send_message
