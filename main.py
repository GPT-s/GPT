import src.crawler

links = ['https://www.investing.com/news/most-popular-news']
text = src.investing_crawl_page(links)
print(text)