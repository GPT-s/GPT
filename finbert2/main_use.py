# main.py
# 메인에서 사용하는 예시

from news_sentiment import crawl_page, analyze_sentiment

# Define the URL of the web page to crawl
url = 'https://finance.yahoo.com/'

# Crawl the web page and perform sentiment analysis on the news articles
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
news = soup.find_all('div', {'class': 'Pos(r) Bgc($bg-content) Bgc($lv2BgColor)! Miw(1007px) Maw(1260px) tablet_Miw(600px)--noRightRail Bxz(bb) Bdstartc(t) Bdstartw(20px) Bdendc(t) Bdends(s) Bdendw(20px) Bdstarts(s) Mx(a)'})

for item in news:
    title = item.find('h3').text
    content = item.find('p').text
    url = item.find('a')['href']
    text = crawl_page(url)  # Crawl the
