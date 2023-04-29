from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import logging
import pymysql
import pymysql.err


os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

class LiveCrawler:
    def __init__(self):
        # from selenium.webdriver.chrome.options import Options
        # Options 클래스는 크롬 웹 드라이버의 동작을 구성하고 사용자 지정 옵션을 설정할 수 있는 기능을 제공
        # 이를 사용하여 웹 드라이버의 다양한 속성을 제어할 수 있음
        # 예를 들어, 브라우저를 headless로 실행하거나 프록시 설정, 창 크기 등을 조정할 수 있음
        # headless 모드는 웹 드라이버가 사용자 인터페이스 없이 백그라운드에서 작동하도록 하는 것으로,
        # 일반적으로 크롤링 작업이나 자동화 시나리오에서 사용
        options = Options()
        options.headless = True  # 이 코드가 창 안보이게 실행하는 거 인듯
        self.driver = webdriver.Chrome(options=options)
    
    # 인베스팅 종목 검색해서 뉴스 링크 가져오고 크롤링해서 출력

    def set_chrome_driver(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        )
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return driver


    # 인베스팅 뉴스 기사 페이지에서 텍스트 가져오는 함수
    def investing_crawl_page(self, url):
        try:
            driver = self.set_chrome_driver(False)
            driver.get(url)
            article_page = driver.find_element(By.CLASS_NAME, "articlePage")
            text = article_page.text
            driver.close()
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
    def investing_search(self,news):
        investing_stock_latest = self.set_chrome_driver(False)
        investing_stock_latest.get("https://www.investing.com/")
        search = investing_stock_latest.find_element(By.CSS_SELECTOR, ".js-main-search-bar")
        search.send_keys(news)  # 텔레그램에서 받아와서 검색할 수 있는 지 알아봐야함
        search.send_keys(Keys.ENTER)
        div_name = investing_stock_latest.find_element(
            By.CSS_SELECTOR, ".js-inner-all-results-quotes-wrapper"
        )
        a_name = div_name.find_element(By.CSS_SELECTOR, "a")
        a_name.click()
        a_name2 = investing_stock_latest.find_element(
            By.CSS_SELECTOR, 'a[data-test="link-news"]'
        )
        a_name2.click()

        investing_stock_latest_links = []

        

        # 링크 가져오는 부분
        for link in investing_stock_latest.find_element(
            By.CLASS_NAME, "mediumTitle1"
        ).find_elements(By.CLASS_NAME, "js-article-item")[:1]:
            investing_stock_latest_links.append(
                link.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            )
        print("링크 가져오기 완")
        investing_stock_latest.quit()
        print("여기까지되는거니?")
        
        for i in investing_stock_latest_links:
            result = i
            print(result)
        # investing_text = self.crawl_links(investing_stock_latest_links, self.investing_crawl_page)
        # # 링크랑 크롤링한 텍스트
        # # result = list(zip(investing_stock_latest_links, investing_text))
        # result = investing_text
        return result