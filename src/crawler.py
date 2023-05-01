# 크롤러
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import os
import logging

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
from database import DataBase
from datetime import datetime
from gpt import get_summary_list
from translator_deepl import DeeplTranslator
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"  # __pycache__ 생성 막는 코드

# # 시간 측정
# start_time = time.time()

class InvestingCrawler:
    def __init__(self):
        print("크롤러 1번 시작")
        driver_path = "/root/GPT/chromedriver"  # Chrome WebDriver의 경로를 지정
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 눈에 보이지 않는 창으로 실행
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        print("크롤러 1번 완")

    def crawl_page(self, url):
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
        

    def investing_latest(self):
        print("크롤러 3번 시작")
        self.driver.get("https://www.investing.com/news/latest-news")
        latest_links = []
        for link in self.driver.find_elements(By.CLASS_NAME, "js-article-item")[:3]:
            latest_links.append(
                link.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            )
        database = DataBase()

        for link in latest_links:
            database.insert_news(link, "", datetime.now())

        latest_news = database.select_news()
        latest_text = []
        for news in latest_news:
            link = news[1]
            text = self.crawl_page(link)
            latest_text.append(text)

        latest_summary = get_summary_list(latest_text)

        translator = DeeplTranslator()
        latest_translated = []

        for summary in latest_summary:
            translated_summary = translator.translate(summary)
            latest_translated.append(translated_summary)

        for i, news in enumerate(latest_news):
            news_id = news[0]
            database.update_news_summary(news_id, latest_translated[i])
        
        self.driver.quit()
        print("크롤링 / 요약 / 번역 저장 완")

        print("크롤러 3번 완")
        return latest_links, latest_text



investingcrawler = InvestingCrawler()
investingcrawler.investing_latest()

# end_time = time.time()
# Total_time = end_time - start_time
# print(f"저장된 뉴스 가져와서 메시지 보내기까지 걸린 시간: {Total_time:.2f} 초")