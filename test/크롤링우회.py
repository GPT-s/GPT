from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import time


# 가짜 User-Agent 정보 생성
user_agent = UserAgent().chrome

# Chrome 브라우저 옵션 설정 - 가짜 userAgent 추가
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')

# Chrome 드라이버 생성
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def set_chrome_driver(headless=True):
    # 가짜 User-Agent 정보 생성
    user_agent = UserAgent().chrome
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def crawl_page(url):
    try:
        driver = set_chrome_driver(False)
        driver.get(url)
        article_page = driver.find_element(By.CLASS_NAME, 'articlePage')
        text = article_page.text
        driver.close()
    except NoSuchElementException:
        text = ""
    return text

while True:
    top5 = set_chrome_driver(False)
    top5.get('https://www.investing.com/news/most-popular-news')

    top5_links = []

    for link in top5.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:5]:
        top5_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

    top5_text = []

    for link in top5_links:

        text = crawl_page(link)
        top5_text.append(text)

        print("크롤링한 기사 출력")
        print(top5_text)
        print()

    top5.close()
    time.sleep(60) # 1분마다 실행

