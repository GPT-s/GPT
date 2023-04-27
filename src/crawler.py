# 크롤러
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# pip install requests beautifulsoup4
# import requests
# from bs4 import BeautifulSoup as bs

# pip install pandas
# import pandas as pd

# from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import os
import logging


os.environ["PYTHONDONTWRITEBYTECODE"] = "1"  # __pycache__ 생성 막는 코드


# 시간 측정
start_time = time.time()


# 창 없이 하는거
class InvestingCrawler:
    def __init__(self):
        # from selenium.webdriver.chrome.options import Options
        # Options 클래스는 크롬 웹 드라이버의 동작을 구성하고 사용자 지정 옵션을 설정할 수 있는 기능을 제공
        # 이를 사용하여 웹 드라이버의 다양한 속성을 제어할 수 있음
        # 예를 들어, 브라우저를 headless로 실행하거나 프록시 설정, 창 크기 등을 조정할 수 있음
        # headless 모드는 웹 드라이버가 사용자 인터페이스 없이 백그라운드에서 작동하도록 하는 것으로,
        # 일반적으로 크롤링 작업이나 자동화 시나리오에서 사용
        # options = Options()
        # options.headless = True  # 이 코드가 창 안보이게 실행하는 거 인듯
        # self.driver = webdriver.Chrome(options=options)  # 웹 드라이버 초기화(눈에 보이지 않는 창으로 실행)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--single-process")

    def crawl_page(self, url):
        try:
            # 새 탭 열기
            self.driver.execute_script("window.open('about:blank', 'new_tab');")
            # 새 탭으로 전환
            self.driver.switch_to.window("new_tab")

            # 주어진 URL로 이동
            self.driver.get(url)

            # 클래스가 articlePage인 요소를 찾아 텍스트 추출
            article_page = self.driver.find_element(By.CLASS_NAME, "articlePage")
            ptag = article_page.find_elements(By.TAG_NAME, "p")

            # 모든 p 태그의 텍스트를 추출하여 리스트에 추가
            text_list = [p.text for p in ptag]

            # 리스트의 모든 요소를 하나의 문자열로 결합
            text = "\n".join(text_list)

            # text = article_page.text
        except NoSuchElementException:
            text = ""  # 요소를 찾지 못한 경우 빈 문자열 반환

        # # 특정 문자열 제거
        # text = text.replace("© Reuters. FILE PHOTO:", "")
        # text = text.replace("© Reuters.", "")

        # 현재 탭 닫기
        self.driver.close()

        # 이전 탭으로 전환
        self.driver.switch_to.window(self.driver.window_handles[0])
        return text

    def investing_latest(self):
        # 최신 뉴스 페이지로 이동
        self.driver.get("https://www.investing.com/news/latest-news")

        # 링크를 저장할 빈 리스트 생성
        latest_10_links = []

        # 상위 10개 기사 링크 수집
        for link in self.driver.find_elements(By.CLASS_NAME, "js-article-item")[:3]:
            latest_10_links.append(
                link.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            )

        # 텍스트를 저장할 빈 리스트 생성
        latest_10_text = []

        # 각 링크에 대해 새 탭에서 크롤링 수행
        for link in latest_10_links:
            # 새 탭에서 페이지 크롤링하고 텍스트 가져오기
            text = self.crawl_page(link)
            # 텍스트를 리스트에 추가
            latest_10_text.append(text)
            print(latest_10_text)
        self.driver.quit()
        print("크롤링 완")
        print("크롤링 완")
        print("크롤링 완")
        

        return latest_10_links, latest_10_text

# 사용예시
crawler = InvestingCrawler()
crawler.investing_latest()

# 현재 작업 디렉토리에 저장
# logging.basicConfig(filename="crawler_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")