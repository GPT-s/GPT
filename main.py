from src.crawler import *

links = ['https://www.investing.com/news/most-popular-news']
text = investing_crawl_page(links)
print(text)