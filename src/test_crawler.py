# 크롤러 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup as bs

from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1' # __pycache__ 생성 막는 코드


# 다른 방식임 새창을 여는게 아니라 새탭에 열어서 크롤링
# 이게 더 빠른거 같기도
# 셀레니움 버전
class Investing_Crawler:
    def __init__(self):
        # 웹 드라이버 초기화
        self.driver = webdriver.Chrome()
    
    # 한 탭에서 페이지 크롤링하는 함수 정의
    def crawl_page_in_tab(self, url):
        try:
            # 새 탭을 연 후, 그 탭으로 전환
            self.driver.execute_script("window.open('about:blank', 'new_tab');")
            self.driver.switch_to.window("new_tab")
            
            # 주어진 URL로 이동
            self.driver.get(url)
            
            # articlePage 클래스를 가진 요소를 찾아 텍스트 추출
            article_page = self.driver.find_element(By.CLASS_NAME, 'articlePage')
            text = article_page.text
        except NoSuchElementException:
            # 요소를 찾지 못하면 빈 문자열 반환
            text=""
        
        # 현재 탭 닫고 이전 탭으로 전환
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return text

    def investing_latest(self):
        self.driver.get('https://www.investing.com/news/latest-news')

        # 링크를 저장할 빈 리스트 생성
        latest_10_links = []

        # 상위 10개 기사 링크 수집
        for link in self.driver.find_elements(By.CLASS_NAME, 'js-article-item')[:10]:
            latest_10_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

        # 텍스트를 저장할 빈 리스트 생성
        latest_10_text = []

        # 각 링크에 대해 새 탭에서 크롤링 수행
        for link in latest_10_links:
            text = self.crawl_page_in_tab(link)
            latest_10_text.append(text)
            
            # 크롤링한 기사 출력
            print("Article crawled:")
            print(text)
            print()

        # 웹 드라이버 종료
        self.driver.quit()

        return latest_10_text

# 사용 예시
crawler = Investing_Crawler()
crawler.investing_latest()


#창 없이 하는거
# class Investing_Crawler:
#     def __init__(self):
#         # from selenium.webdriver.chrome.options import Options
#         # Options 클래스는 크롬 웹 드라이버의 동작을 구성하고 사용자 지정 옵션을 설정할 수 있는 기능을 제공
#         # 이를 사용하여 웹 드라이버의 다양한 속성을 제어할 수 있음
#         # 예를 들어, 브라우저를 headless로 실행하거나 프록시 설정, 창 크기 등을 조정할 수 있음
#         # headless 모드는 웹 드라이버가 사용자 인터페이스 없이 백그라운드에서 작동하도록 하는 것으로, 
#         # 일반적으로 크롤링 작업이나 자동화 시나리오에서 사용
#         options = Options()
#         options.headless = True # 이 코드가 창 안보이게 실행하는 거 인듯
#         self.driver = webdriver.Chrome(options=options)  # 웹 드라이버 초기화(눈에 보이지 않는 창으로 실행)
    
#     def crawl_page_in_tab(self, url):
#         try:
#             # 새 탭 열기
#             self.driver.execute_script("window.open('about:blank', 'new_tab');")
#             # 새 탭으로 전환
#             self.driver.switch_to.window("new_tab")
            
#             # 주어진 URL로 이동
#             self.driver.get(url)
            
#             # 클래스가 articlePage인 요소를 찾아 텍스트 추출
#             article_page = self.driver.find_element(By.CLASS_NAME, 'articlePage')
#             text = article_page.text
#         except NoSuchElementException:
#             text=""   # 요소를 찾지 못한 경우 빈 문자열 반환

#         # 현재 탭 닫기
#         self.driver.close()  
#          # 이전 탭으로 전환
#         self.driver.switch_to.window(self.driver.window_handles[0])
#         return text

#     def investing_latest(self):
#         # 최신 뉴스 페이지로 이동
#         self.driver.get('https://www.investing.com/news/latest-news')

#         # 링크를 저장할 빈 리스트 생성
#         latest_10_links = []

#         # 상위 10개 기사 링크 수집
#         for link in self.driver.find_elements(By.CLASS_NAME, 'js-article-item')[:5]:
#             latest_10_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

#         # 텍스트를 저장할 빈 리스트 생성
#         latest_10_text = []

#         cnt = 1
#         # 각 링크에 대해 새 탭에서 크롤링 수행
#         for link in latest_10_links:
#             # 새 탭에서 페이지 크롤링하고 텍스트 가져오기
#             text = self.crawl_page_in_tab(link)
#             # 텍스트를 리스트에 추가
#             latest_10_text.append(text)
            
#             print("────────────────────────────────────────────────────────────────────────────")
#             print(f"최신 기사 {cnt}")
#             print()
#             print(text)
#             print()
#             print("────────────────────────────────────────────────────────────────────────────")
#             cnt += 1
#         self.driver.quit()

#         return latest_10_text

# # 사용 예시
# # Investing_Crawler 클래스의 인스턴스 생성
# crawler = Investing_Crawler()
#  # investing_latest 메서드 호출하여 기사 크롤링하고 출력
# crawler.investing_latest()