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


class Crawler:
    def __init__(self):
        self.driver = self.set_chrome_driver(False)

    def set_chrome_driver(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    # 인베스팅 뉴스 기사 페이지에서 텍스트 가져오는 함수
    def investing_crawl_page(self, url):
        try:
            self.driver.get(url)
            article_page = self.driver.find_element(By.CLASS_NAME, 'articlePage')
            text = article_page.text
            self.driver.close()
        except NoSuchElementException:
            text = ""
        return text


    # 여러 링크를 한번에 띄우고 크롤링하는 함수 작동원리는 공부 좀 해야할 듯
    def crawl_links(self, links, crawl_func):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(crawl_func, link) for link in links]
            results = [future.result() for future in as_completed(futures)]
        return results


    # 인베스팅 종목 검색해서 뉴스 링크 가져오고 크롤링해서 출력
    def investing_search(self):
        investing_latest = self.set_chrome_driver(False)
        investing_latest.get('https://www.investing.com/')
        search = investing_latest.find_element(By.CSS_SELECTOR, '.js-main-search-bar')
        search.send_keys('tsla') # 텔레그램에서 받아와서 검색할 수 있는 지 알아봐야함
        search.send_keys(Keys.ENTER)
        div_name = investing_latest.find_element(By.CSS_SELECTOR, '.js-inner-all-results-quotes-wrapper')
        a_name = div_name.find_element(By.CSS_SELECTOR, 'a')
        a_name.click()
        a_name2 = investing_latest.find_element(By.CSS_SELECTOR, 'a[data-test="link-news"]')
        a_name2.click()

        investing_latest_links = []

        for link in investing_latest.find_element(By.CLASS_NAME, 'mediumTitle1').find_elements(By.CLASS_NAME, 'js-article-item')[:5]:
            investing_latest_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        investing_latest.quit()

        investing_text = self.crawl_links(investing_latest_links, self.investing_crawl_page)

        # print("인베스팅 검색 후 크롤링")
        # for text in investing_text:
        #     print(text)
        #     print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
        return investing_text


def main():
    crawler = Crawler()
    crawler.investing_search()

main()