# 크롤러 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from concurrent.futures import ThreadPoolExecutor, as_completed



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

# 야후 파이낸스 뉴스 기사 페이지에서 텍스트 가져오는 함수
def yahoo_crawl_page(url):
    try:
        driver = set_chrome_driver(False)
        driver.get(url)
        article_page = driver.find_element(By.CLASS_NAME, 'wafer-sticky')
        text = article_page.text
        driver.close()
    except NoSuchElementException:
        text = ""
    return text


# 여러 링크를 한번에 크롤링하는 함수 작동원리는 공부 좀 해야할듯
def crawl_links(links, crawl_func):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(crawl_func, link) for link in links]
        results = [future.result() for future in as_completed(futures)]
    return results


# 인베스팅 뉴스 링크 가져오고 크롤링해서 출력
def investing_news():
    investing_top3 = set_chrome_driver(False)
    investing_top3.get('https://www.investing.com/news/most-popular-news')
    investing_top3_links = []
    for link in investing_top3.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:3]:
        investing_top3_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    investing_top3.quit()

    investing_top3_text = crawl_links(investing_top3_links, investing_crawl_page)

    print("인베스팅 Top3")
    for text in investing_top3_text:
        print(text)
        print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')


# 야후 파이낸스 뉴스 링크 가져오고 크롤링해서 출력
def yahoo_news():
    yahoo_latest = set_chrome_driver(False)
    yahoo_latest.get('https://finance.yahoo.com/news/')
    yahoo_latest_links = []
    for link in yahoo_latest.find_element(By.ID, 'Fin-Stream-Proxy').find_elements(By.CLASS_NAME, 'js-stream-content')[:3]:
        yahoo_latest_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    yahoo_latest.quit()
    
    yahoo_latest_text = crawl_links(yahoo_latest_links, yahoo_crawl_page)

    print("야후 파이낸스 최신뉴스")
    for text in yahoo_latest_text:
        print(text)
        print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')


if __name__ == '__main__':
    investing_news()
    yahoo_news()

