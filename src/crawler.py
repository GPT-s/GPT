# 크롤러
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import asyncio
import logging
import sentry_sdk
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
DSN = os.environ.get("DSN")

dsn = DSN
sentry_sdk.init(
    dsn=DSN,
)

class InvestingCrawler:
    def __init__(self):
        """InvestingCrawler 객체 초기화"""
        try:
            self.driver = self.init_driver()
        except Exception as e:
            logging.error(f"웹드라이버 초기화 중 에러 발생: {e}")
            sentry_sdk.capture_exception(e)

    def init_driver(self) -> webdriver.Chrome:
        """
        웹드라이버를 초기화하고 반환합니다.

        Returns:
            webdriver.Chrome: 초기화된 Chrome 웹드라이버 객체
        """
        print("크롤러 1번 시작")
        driver = None
        try:
            driver_path = "/root/GPT/chromedriver"
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument('--disable-dev-shm-usage')
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logging.error(f"웹드라이버 초기화 중 에러 발생: {e}")
            sentry_sdk.capture_exception(e)
        finally:
            print("크롤러 1번 완")
            return driver
    
    async def crawl_page(self, url: str) -> str:
        """
        주어진 URL의 웹 페이지를 크롤링합니다.

        Args:
            url (str): 크롤링할 웹 페이지의 URL

        Returns:
            str: 크롤링한 웹 페이지의 텍스트
        """
        print("크롤러 2번 시작")
        text = None
        try:
            self.driver.execute_script("window.open('about:blank', 'new_tab');")
            self.driver.switch_to.window("new_tab")
            self.driver.get(url)
            article_page = self.driver.find_element(By.CLASS_NAME, "articlePage")
            ptag = article_page.find_elements(By.TAG_NAME, "p")
            text_list = [p.text for p in ptag]
            text = "\n".join(text_list)
        except NoSuchElementException:
            logging.error("크롤링 중 요소를 찾지 못했습니다.")
            sentry_sdk.capture_exception(Exception("크롤링 중 요소를 찾지 못했습니다."))
        except Exception as e:
            logging.error(f"크롤링 중 에러 발생: {e}")
            sentry_sdk.capture_exception(e)
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("크롤러 2번 완")
            return text
        
    async def get_latest_links(self) -> List[str]:
        """
        최신 뉴스 링크들을 크롤링합니다.

        Returns:
            List[str]: 크롤링된 최신 뉴스 링크들의 리스트
        """
        print("링크 크롤링 시작")
        latest_links = []
        try:
            self.driver.get("https://www.investing.com/news/latest-news")
            for link in self.driver.find_elements(By.CLASS_NAME, "js-article-item")[:3]:
                latest_links.append(
                    link.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                )
        except Exception as e:
            logging.error(f"크롤링 중 에러 발생: {e}")
            sentry_sdk.capture_exception(e)
        finally:
            print("링크 크롤링 완")
            return latest_links

    async def get_latest_texts(self, links: List[str]) -> List[str]:
        """
        주어진 링크들의 웹 페이지를 크롤링합니다.

        Args:
            links (List[str]): 크롤링할 웹 페이지 링크들의 리스트

        Returns:
            List[str]: 크롤링한 각 웹 페이지의 텍스트들의 리스트
        """
        print("텍스트 크롤링 시작")
        tasks = []
        try:
            for link in links:
                tasks.append(asyncio.create_task(self.crawl_page(link)))
            texts = await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f"텍스트 크롤링 중 에러 발생: {e}")
            sentry_sdk.capture_exception(e)
        finally:
            self.driver.close()
            print("텍스트 크롤링 완")
            return texts
    
   
#     # main
# async def main() :
#     crawler = InvestingCrawler()
#     links = await crawler.get_latest_links()
#     texts = await crawler.get_latest_texts(links)
#     print(texts)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
    

    