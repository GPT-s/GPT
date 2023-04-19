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


def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# 인베스팅 뉴스 기사 페이지에서 텍스트 가져오는 함수
def investing_crawl_page(url):
    try:
        driver = set_chrome_driver(False)
        driver.get(url)
        article_page = driver.find_element(By.CLASS_NAME, 'articlePage')
        text = article_page.text
        driver.close()
    except NoSuchElementException:
        text = ""
    return text


# 여러 링크를 한번에 띄우고 크롤링하는 함수 작동원리는 공부 좀 해야할 듯
def crawl_links(links, crawl_func):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(crawl_func, link) for link in links]
        results = [future.result() for future in as_completed(futures)]
    return results


# 인베스팅 종목 검색해서 뉴스 링크 가져오고 크롤링해서 출력
def investing_search():
    investing_stock_latest = set_chrome_driver(False)
    investing_stock_latest.get('https://www.investing.com/')
    search = investing_stock_latest.find_element(By.CSS_SELECTOR, '.js-main-search-bar')
    search.send_keys('tsla') # 텔레그램에서 받아와서 검색할 수 있는 지 알아봐야함
    search.send_keys(Keys.ENTER)
    div_name = investing_stock_latest.find_element(By.CSS_SELECTOR, '.js-inner-all-results-quotes-wrapper')
    a_name = div_name.find_element(By.CSS_SELECTOR, 'a')
    a_name.click()
    a_name2 = investing_stock_latest.find_element(By.CSS_SELECTOR, 'a[data-test="link-news"]')
    a_name2.click()

    investing_stock_latest_links = []

    for link in investing_stock_latest.find_element(By.CLASS_NAME, 'mediumTitle1').find_elements(By.CLASS_NAME, 'js-article-item')[:2]:
        investing_stock_latest_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    investing_stock_latest.quit()

    investing_text = crawl_links(investing_stock_latest_links, investing_crawl_page)

    # Combine links with the crawled text
    result = list(zip(investing_stock_latest_links, investing_text))

    return result

    # print("인베스팅 검색 후 크롤링")
    # for text in investing_text:
    #     print()
    #     print(text)
    #     print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')

def investing_latest_news():
    driver = set_chrome_driver(False)
    driver.get('https://www.investing.com/news/latest-news')

    latest_links = []

    for link in driver.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:3]:
        latest_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    driver.quit()

    news_text = crawl_links(latest_links, investing_crawl_page)

    result = list(news_text)
    # news_text = crawl_links(latest_links, investing_crawl_page)

    # result = list(zip(latest_links, news_text))

    return result

def deepL_Translator(text):
    try:
        deepL = set_chrome_driver(False)  # Chrome 웹 드라이버 설정
        deepL.get('https://www.deepl.com/ko/translator')  # 딥엘 번역 페이지로 이동
        time.sleep(2) # 텍스트 입력이나 변역된 텍스트 가져오기 전에 페이지를 닫아서
        deepL.find_element(By.CSS_SELECTOR, '.lmt__textarea.lmt__source_textarea.lmt__textarea_base_style').send_keys(text)
        time.sleep(2)
        deepL_translated = deepL.find_element(By.CSS_SELECTOR, '.lmt__target_textarea')   # 번역된 텍스트 요소 찾기
        time.sleep(5)
        result = deepL_translated.get_attribute('value')   # 번역된 텍스트 추출
    except NoSuchElementException: # 예외처리 (요소를 찾지 못하는 경우)
        result = '번역 오류ㅠㅠ'   # 번역 오류 메시지 설정
    finally:
        deepL.close()  # 웹 드라이버 종료
    return result  # 번역된 결과 반환


# from crawler import investing_search 

# investing_search = investing_search()

# for text in investing_search:
#     print(f"최신 기사")
#     print(text)
#     print("\n---\n")

# investing_latest_news = investing_latest_news()

# for text in investing_latest_news:
#     print(f"최신 기사")
#     print(text)
#     print("\n---\n")
