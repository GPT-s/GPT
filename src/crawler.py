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
    
