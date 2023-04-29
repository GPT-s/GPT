from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
# import requests
# from bs4 import BeautifulSoup as bs
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import os
import logging
import pymysql
import pymysql.err

import asyncio

class InvestingCrawler:
    def __init__(self):
        driver_path = "/root/GPT/chromedriver"  # Chrome WebDriver의 경로를 지정
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 눈에 보이지 않는 창으로 실행
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    async def crawl_page(self, url):
        try:
            self.driver.execute_script("window.open('about:blank', 'new_tab');")
            self.driver.switch_to.window("new_tab")

            self.driver.get(url)

            article_page = self.driver.find_element(By.CLASS_NAME, "articlePage")
            ptag = article_page.find_elements(By.TAG_NAME, "p")

            text_list = [p.text for p in ptag]
            text = "\n".join(text_list)

        except NoSuchElementException:
            text = ""

        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])
        return text

    async def investing_latest(self):
        self.driver.get("https://www.investing.com/news/latest-news")

        latest_10_links = []

        for link in self.driver.find_elements(By.CLASS_NAME, "js-article-item")[:10]:
            latest_10_links.append(
                link.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            )

        latest_10_text = []

        tasks = [self.crawl_page(link) for link in latest_10_links]
        results = await asyncio.gather(*tasks)

        # cnt = 1
        # for text in results:
        #     latest_10_text.append(text)

        #     logging.info(f"────────────────────────────────────────────────────────────────────────────")
        #     logging.info(f"최신 기사 {cnt}")
        #     logging.info(text)
        #     logging.info(f"────────────────────────────────────────────────────────────────────────────")
        #     cnt += 1

        self.driver.quit()
        print("크롤링 완료")

        return latest_10_links, latest_10_text

# 메인에 작성
async def main():
    crawler = InvestingCrawler()
    result = await crawler.investing_latest()
    return result

if __name__ == "__main__":
    logging.basicConfig(filename="crawler_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    asyncio.run(main())
