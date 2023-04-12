#!/usr/bin/env python
# coding: utf-8

# In[7]:


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from chrome_driver import set_chrome_driver

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

