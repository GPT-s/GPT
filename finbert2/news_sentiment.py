# news_sentiment.py

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def set_chrome_driver(headless):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(options=options)
    return driver

def crawl_page(url):
    try:
        driver = set_chrome_driver(False) 
        driver.get(url)  
        article_page = driver.find_element_by_class_name('articlePage')
        text = article_page.text 
        driver.close() 
    except NoSuchElementException: 
        text = ""  
    return text  

from transformers import pipeline

def analyze_sentiment(text):
    l
    model_name = "ProsusAI/finbert"
    classifier = pipeline('sentiment-analysis', model=model_name)
    result = classifier(text)[0]
    label = result['label']
    scores = result['score']
    return label, scores
