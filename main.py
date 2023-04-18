import src.crawler
import src.finbert
import src.gpt
import src.gpt_sent
import src.stock_idx
import src.telegram_handler
#import sys
#import os

#src_path = os.path.abspath("src")
#sys.path.append(src_path)


links = ['https://www.investing.com/news/most-popular-news']
text = investing_crawl_page(links)
print(text)