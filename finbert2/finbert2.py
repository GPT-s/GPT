from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


"""
To install a library, run the following command: 
!pip install library_name
"""
import warnings
warnings.filterwarnings('ignore') # to avoid warnings

import random
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

"""
Sklearn Libraries
"""
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

"""
Transformer Libraries
"""

from transformers import BertTokenizer, AutoModelForSequenceClassification, AdamW, get_linear_schedule_with_warmup

"""
Pytorch Libraries
"""
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler


import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# 크롬드라이버 셋팅
def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        # GUI 없이 Chrome 드라이버를 실행하기 위해 headless 모드 설정
        options.add_argument('headless') 
    # 브라우저와 유사한 user-agent 설정
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
     # 지정된 옵션으로 Chrome 웹 드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
    return driver

# 뉴스 페이지 크롤링
def crawl_page(url):
    try:
        driver = set_chrome_driver(False) # Chrome 웹 드라이버 인스턴스 생성
        driver.get(url)  # 지정된 URL을 웹 드라이버에서 열기
        # 요소 변경 가능
        article_page = driver.find_element(By.CLASS_NAME, 'articlePage') # class 이름으로 뉴스 기사 페이지 요소 찾기
        text = article_page.text # 뉴스 기사 페이지 요소에서 텍스트 추출
        driver.close() # 텍스트 추출 후 웹 드라이버 닫기
    except NoSuchElementException: 
        text = ""  # 뉴스 기사 페이지 요소가 없을 경우 텍스트를 빈 문자열로 설정
    return text  # 추출된 텍스트 반환



import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from selenium.webdriver.common.by import By

# Load FinBERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')

# Define the function to crawl the web page
def crawl_page(url):
    try:
        driver = webdriver.Chrome() # Chrome 웹 드라이버 인스턴스 생성
        driver.get(url)  # 지정된 URL을 웹 드라이버에서 열기
        # 요소 변경 가능
        article_page = driver.find_element(By.CLASS_NAME, 'articlePage') # class 이름으로 뉴스 기사 페이지 요소 찾기
        text = article_page.text # 뉴스 기사 페이지 요소에서 텍스트 추출
        driver.close() # 텍스트 추출 후 웹 드라이버 닫기
    except NoSuchElementException: 
        text = ""  # 뉴스 기사 페이지 요소가 없을 경우 텍스트를 빈 문자열로 설정
    return text  # 추출된 텍스트 반환

def analyze_sentiment(text):
    # Tokenize the text and convert to input IDs
    input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')

    # Run the input IDs through the model and decode the outputs
    with torch.no_grad():
        output = model(input_ids)
    scores = output[0][0]
    logits = scores.detach().numpy()
    label = "Neutral"
    if logits[0] > logits[1]:
        label = "Negative"
    elif logits[0] < logits[1]:
        label = "Positive"
    return label, logits


# Define the URL of the web page to crawl
url = 'https://finance.yahoo.com/'

# Crawl the web page and perform sentiment analysis on the news articles
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
news = soup.find_all('div', {'class': 'Pos(r) Bgc($bg-content) Bgc($lv2BgColor)! Miw(1007px) Maw(1260px) tablet_Miw(600px)--noRightRail Bxz(bb) Bdstartc(t) Bdstartw(20px) Bdendc(t) Bdends(s) Bdendw(20px) Bdstarts(s) Mx(a)'})

for item in news:
    title = item.find('h3').text
    content = item.find('p').text
    text = crawl_page(url)  # Crawl the web page to get the full text of the news article
    label, scores = analyze_sentiment(text)  # Analyze the sentiment of the news article
    print('Title:', title)
    print('Content:', content)
    print('Sentiment:', label)
    print('--------------------------')




# 리스트 형태로 출력
results = []

# Loop through the news articles and perform sentiment analysis on each one
for item in news:
    title = item.find('h3').text
    content = item.find('p').text
    url = item.find('a')['href']
    text = crawl_page(url)
    label, _ = analyze_sentiment(text)
    
    # Add the results to the list
    result = {'title': title, 'content': content, 'label': label}
    results.append(result)

# Print the results
for result in results:
    print(result)

