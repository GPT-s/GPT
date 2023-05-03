# 크롤러
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import os
import asyncio
import logging
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# from src.database import DataBase
# from datetime import datetime
# from src.gpt import get_summary_list
# from src.translator_deepl import DeeplTranslator
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
from database import DataBase
from datetime import datetime
from typing import List

class InvestingCrawler:
    def __init__(self):
        self.driver = self.init_driver()
        # self.translator = DeeplTranslator()

    def init_driver(self)-> webdriver.Chrome:
        """웹드라이버 초기화 및 반환"""
        print("크롤러 1번 시작")
        driver_path = "/root/GPT/chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print("크롤러 1번 완")
        return driver
    
    async def crawl_page(self, url: str) -> str:
        """특정 URL의 웹 페이지 크롤링"""
        print("크롤러 2번 시작")
        try:
            self.driver.execute_script("window.open('about:blank', 'new_tab');")
            self.driver.switch_to.window("new_tab")

            self.driver.get(url)

            article_page = self.driver.find_element(By.CLASS_NAME, "articlePage")
            ptag = article_page.find_elements(By.TAG_NAME, "p")

            text_list = [p.text for p in ptag]

            text = "\n".join(text_list)
           
        except NoSuchElementException:
            text = None
        except Exception as e:
            logging.ERROR(f"crawl_page error: {e}")
            text = None
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("크롤러 2번 완")
            return text
        
    async def get_latest_links(self):
        self.driver.get("https://www.investing.com/news/latest-news")
        latest_links = []
        for link in self.driver.find_elements(By.CLASS_NAME, "js-article-item")[:3]:
            latest_links.append(
                link.find_element(By.CSS_SELECTOR, "a").get_attribute("href"))
            print("링크 크롤링 완")
        return latest_links

    async def get_latest_texts(self, links):
        tasks = []
        for link in links:
            tasks.append(asyncio.create_task(self.crawl_page(link)))
        texts = await asyncio.gather(*tasks)
        self.driver.close()
        print("텍스트 크롤링 완")
        return texts
    
   
    # main
# async def main() :
#     crawler = InvestingCrawler()
#     links = await crawler.get_latest_links()
#     texts = await crawler.get_latest_texts(links)
#     print(texts)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
    

    