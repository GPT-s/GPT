from src.crawler import InvestingCrawler
import src.crawler
from src.finbert import FinBert
from src.gpt import summarize
#import src.gpt_sent
#import src.stock_idx  
#from src.telegram_handler import TelegramHandler
import src.telegram_handler
from src.gpt_keyword import get_analyze_keyword, analyze_keyword
from src.database import DataBase
# 메인 업데이트 

#send_message = TelegramHandler()
investing_latest_news = InvestingCrawler()
finbert = FinBert()
send_message = src.telegram_handler # 클래스화 전 텔레그램 
translate = src.crawler # 크롤러 모듈 내부 번역기 사용 전용 변수

#insert_data_user = DataBase().insert_user('5999372705','F')
#update_data_sub = DataBase().update_user('5999372705', 'T')
#update_data_nosub = DataBase().update_user('5999372705', 'F')



class Main:

        if send_message.telegram_main().equals('/start'): # 사용자가 챗봇 생성 시 실행
                insert_data_user = DataBase().insert_user('5611753679','F')
                insert_data_user
                send_message.send_message('5611753679', '아이디 생성 완료')
                #실행 됨.

        elif send_message.telegram_main().equals('/sub'): # 사용자가 sub 명령어 입력 시 실행
                update_data_sub = DataBase().update_user('5611753679', 'T')
                update_data_sub
                #send_message.send_message('5999372705', '구독하기')

<<<<<<< HEAD
        elif send_message.telegram_main().equals('/nosub'): # 사용자가 nosub 명령어 입력 시 실행
                update_data_nosub = DataBase().update_user('5611753679', 'F')
                update_data_nosub
                #send_message.send_message('5999372705', '구독취소')
=======
        # elif send_message.telegram_main().equals('/nosub'): # 사용자가 nosub 명령어 입력 시 실행
        #         update_data_nosub = DataBase().update_user('5611753679', 'F')
        #         update_data_nosub
                    #send_message.send_message('5999372705', '구독취소')
>>>>>>> 9603bec75dd045b5b436e6b7d64499be11809438

        elif send_message.send_message().equals(send_message.message_handler): # 사용자가 뉴스 데이터 요청 시 실행

            for text in investing_latest_news: # 사용자 요청 시 실행하는 부분
                    result_sentiment = finbert.sentiment(text)# 핀버트 감성 분석 변수
                    result_gpt = summarize(text) # 지피티 요약 변수
                    print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
                    translator = translate.deepL_Translator(result_gpt)
                    telegram_send_message = send_message.send_message('5611753679', text =f"**요약된 뉴스**\n{translator}\n\n**뉴스 링크**\n\n{text}") # 해당 아이디의 텔레그램에 내용 전송
                    telegram_send_message
        #if send_message.telegram_main().equals('/종료'):
        #   print('챗봇을 종료합니다.')
            

