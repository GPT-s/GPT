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
# from concurrent.futures import ThreadPoolExecutor, as_completed 이거 import 해서 그런가
def crawl_links(links, crawl_func):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(crawl_func, link) for link in links]
        results = [future.result() for future in as_completed(futures)]
    return results


# 링크 가져오는 거
def investing_links():
    driver = set_chrome_driver(False)
    driver.get('https://www.investing.com/news/most-popular-news')
    top3_links = []
    for link in driver.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:3]:
        top3_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    driver.quit()
    return top3_links

# 출력
def print_news(links, crawl_func):
    news_text = crawl_links(links, crawl_func)
    print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
    print("인베스팅 Top3")
    for text in news_text:
        print(text)
        print('─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')

# 링크 가져온 거랑 출력하는 거 한 번에 실행
def crawler_main():
    links = investing_links()
    print_news(links, investing_crawl_page)

crawler_main()
