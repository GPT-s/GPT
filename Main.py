#!/usr/bin/env python
# coding: utf-8

# In[4]:


from chrome_driver import set_chrome_driver
from news_crawler import crawl_page
from text_summarizer import summarize
from selenium.webdriver.common.by import By

top5 = set_chrome_driver(False)
top5.get('https://www.investing.com/news/most-popular-news')

top5_links = []

for link in top5.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:5]:
    top5_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

top5_summaries = []

for link in top5_links:
    text = crawl_page(link)
    summary = summarize(text)
    top5_summaries.append(summary)
    
    print("요약 후 번역")
    print(summary)
    print()

