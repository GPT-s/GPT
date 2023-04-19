# 크롤러 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1' # __pycache__ 생성 막는 코드


class Crawler_Search:
    def __init__(self):
        self.driver = self.set_chrome_driver(False)

    def set_chrome_driver(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return self.driver

    # 인베스팅 뉴스 기사 페이지에서 텍스트 가져오는 함수
    def investing_crawl_page(self, url):
        try:
            self.driver.get(url)
            article_page = self.driver.find_element(By.CLASS_NAME, 'articlePage')
            text = article_page.text
            self.driver.close()
        except NoSuchElementException:
            text = ""
        return self.text


    # 여러 링크를 한번에 띄우고 크롤링하는 함수 작동원리는 공부 좀 해야할 듯
    def crawl_links(self, links, crawl_func):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(crawl_func, link) for link in links]
            results = [future.result() for future in as_completed(futures)]
        return self.results


    # 인베스팅 종목 검색해서 뉴스 링크 가져오고 크롤링해서 출력
    def investing_search(self):
        self.driver.get('https://www.investing.com/')
        search = self.driver.find_element(By.CSS_SELECTOR, '.js-main-search-bar')
        search.send_keys('AAPL') # 텔레그램에서 받아와서 검색할 수 있는 지 알아봐야함
        search.send_keys(Keys.ENTER)
        div_name = self.driver.find_element(By.CSS_SELECTOR, '.js-inner-all-results-quotes-wrapper')
        a_name = div_name.find_element(By.CSS_SELECTOR, 'a')
        a_name.click()
        a_name2 = self.driver.find_element(By.CSS_SELECTOR, 'a[data-test="link-news"]')
        a_name2.click()

        investing_latest_links = []

        for link in self.driver.find_element(By.CLASS_NAME, 'mediumTitle1').find_elements(By.CLASS_NAME, 'js-article-item')[:5]:
            investing_latest_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        time.sleep(5)
        self.driver.quit()

        self.investing_text = self.crawl_links(investing_latest_links, self.investing_crawl_page)

        print("인베스팅 검색 후 크롤링")
        for text in self.investing_text:
            print(text)
            print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
        return self.investing_text

# class Crawler_latest:
#     def __init__(self):
#         self.driver = self.se

#     # 한 탭에서 페이지 크롤링하는 함수 정의
#     def crawl_page_in_tab(driver, url):
#         try:
#             # 새 탭을 연 후, 그 탭으로 전환
#             driver.execute_script("window.open('about:blank', 'new_tab');")
#             driver.switch_to.window("new_tab")
            
#             # 주어진 URL로 이동
#             driver.get(url)
            
#             # articlePage 클래스를 가진 요소를 찾아 텍스트 추출
#             article_page = driver.find_element(By.CLASS_NAME, 'articlePage')
#             text = article_page.text
#         except NoSuchElementException:
#             # 요소를 찾지 못하면 빈 문자열 반환
#             text = ""
        
#         # 현재 탭 닫고 이전 탭으로 전환
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#         return text

#     # 웹 드라이버 설정
#     top5 = set_chrome_driver(False)
#     top5.get('https://www.investing.com/news/most-popular-news')

#     # 링크를 저장할 빈 리스트 생성
#     top5_links = []

#     # 상위 10개의 기사 링크 수집
#     for link in top5.find_elements(By.CLASS_NAME, 'js-article-item')[:10]:
#         top5_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

#     # 텍스트를 저장할 빈 리스트 생성
#     top5_text = []

#     # 각 링크에 대해 새 탭에서 크롤링 수행
#     for link in top5_links:
#         text = crawl_page_in_tab(top5, link)
#         top5_text.append(text)
        
#         # 크롤링한 기사 출력
#         print("크롤링한 기사:")
#         print(text)
#         print()

#     # 웹 드라이버 종료
#     top5.quit()


def main():
    crawler = Crawler_Search()
    crawler.investing_search()

main()