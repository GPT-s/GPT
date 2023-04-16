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



# 크롤링 할 url
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