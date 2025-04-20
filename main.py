import requests
from bs4 import BeautifulSoup
from datetime import datetime

UPLOAD_URL = "https://udontech-api.onrender.com/api/upload"
NEWS_URL = "https://www.udontech.ac.th/web66/index.php/2015-08-18-07-06-23"

def fetch_news():
    res = requests.get(NEWS_URL)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    news_items = []

    for article in soup.select('.item'):
        title_tag = article.select_one('h2 a')
        date_tag = article.select_one('.createdate')

        if title_tag and date_tag:
            title = title_tag.text.strip()
            link = title_tag['href']
            date_str = date_tag.text.strip()
            try:
                date_obj = datetime.strptime(date_str, "%d %B %Y")
                timestamp = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                timestamp = date_str  # ใช้รูปแบบเดิมถ้าแปลงไม่สำเร็จ

            news_items.append({
                "type": "ข่าวประชาสัมพันธ์",
                "title": title,
                "description": "ดูรายละเอียดเพิ่มเติมที่เว็บไซต์",
                "link": link,
                "timestamp": timestamp
            })

    return news_items

def upload_news(news_list):
    for item in news_list:
        res = requests.post(UPLOAD_URL, json=item)
        print(f"อัปโหลด {item['title']} → Status {res.status_code}")

if __name__ == "__main__":
    news = fetch_news()
    upload_news(news)
