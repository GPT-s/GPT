# 크롤러 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



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

investing_top3 = set_chrome_driver(False)
investing_top3.get('https://www.investing.com/news/most-popular-news')

investing_top3_links = []

for link in investing_top3.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:3]:
    investing_top3_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

investing_top3_text = []

for link in investing_top3_links:
    
    text = investing_crawl_page(link)
    investing_top3_text.append(text)
    
    print("크롤링한 기사 출력")
    print(investing_top3_text)
    print()
    

yahoo_latest = set_chrome_driver(False)
yahoo_latest.get('https://finance.yahoo.com/news/')

yahoo_latest_links = []

for link in yahoo_latest.find_element(By.ID, 'Fin-Stream-Proxy').find_elements(By.CLASS_NAME, 'js-stream-content')[:3]:
    yahoo_latest_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    print()
    print(yahoo_latest_links)
    print()

yahoo_latest_text = []

for link in yahoo_latest_links:

    text = yahoo_crawl_page(link)
    yahoo_latest_text.append(text)

    print()
    print("야후 기사 출력")
    print()
    print(yahoo_latest_text)
    print()