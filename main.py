import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# URL ของ API ที่ Render สร้างไว้
UPLOAD_API_URL = "https://udontech-api.onrender.com/api/upload"  # เปลี่ยนตาม URL จริงที่คุณได้จาก Render

# -------------------------------
# ดึงข้อมูลจากเว็บไซต์วิทยาลัย
def scrape_udontech():
    url = "https://www.udontech.ac.th"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # ตัวอย่าง: ดึงหัวข้อข่าวล่าสุด
    news_items = soup.select(".elementor-post__title > a")[:5]
    news = [{"title": item.text.strip(), "url": item['href']} for item in news_items]

    return {
        "source": "udontech",
        "timestamp": datetime.now().isoformat(),
        "news": news
    }

# -------------------------------
# ดึงข้อมูลจากเพจ Facebook (public scraping แบบง่าย)
def scrape_facebook():
    fb_url = "https://www.facebook.com/share/16dUr6XDPs/"  # หรือหน้าเพจจริง
    response = requests.get(fb_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # หมายเหตุ: การดึงข้อมูลจาก Facebook โดยตรงมักจะโดนบล็อก ต้องใช้ Facebook API จริงจัง
    # ดังนั้นที่นี่ใช้เป็น placeholder
    posts = [{"text": "Facebook scraping requires API access.", "url": fb_url}]
    
    return {
        "source": "facebook",
        "timestamp": datetime.now().isoformat(),
        "posts": posts
    }

# -------------------------------
# รวมข้อมูลและอัปโหลด
def upload_data():
    udontech_data = scrape_udontech()
    facebook_data = scrape_facebook()

    combined_data = {
        "college_data": udontech_data,
        "facebook_data": facebook_data,
        "collected_at": datetime.now().isoformat()
    }

    # ส่งไปยัง API
    try:
        res = requests.post(UPLOAD_API_URL, json=combined_data)
        if res.status_code == 200:
            print("✅ อัปโหลดข้อมูลสำเร็จ")
        else:
            print("❌ อัปโหลดล้มเหลว:", res.text)
    except Exception as e:
        print("❌ เกิดข้อผิดพลาด:", str(e))

# -------------------------------
if __name__ == "__main__":
    upload_data()
