from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.amazon.co.uk"

def search_url(term: str, page: int = 1) -> str: 
    return f"{BASE_URL}/s?k={term}&page={page}"

HEADERS = {
# "Host": "www.amazon.co.uk",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
# "Accept-Language": "en-GB,en;q=0.5",
# "Accept-Encoding": "gzip, deflate, br",
# "Referer": "https://www.amazon.co.uk/s?k=aaa&page=1",
# "DNT": "1",
# "Connection": "keep-alive",
# "Cookie": 'session-id=262-1842978-9544710; session-id-time=2082787201l; i18n-prefs=GBP; csm-hit=tb:s-HJDT1ZFW5DTCJC1QX8BD|1629919883593&t:1629919885753&adb:adblk_no; ubid-acbuk=259-7037632-9005606; session-token="yaFVW1jB/hz1KcfO9w5MZS8LtJM2I+aB/6OyWYIY7XU7eTjjivKhxbBt72YEzp0+/6l8Agh5NOC9SaP/KYhJiexVaXmDPPktvhz4WdBglU6hurOak2/gFoUHIZ4L8c0FoJcdf8QOOJ9ZedkNNXo+2MlHZgM5jMBiTlozd42vje+brOkYkQpf5UrA5iY+QXratrqdZSjVttuKbpkubV6ycERTs8ibbTrFky2rOCeRKu4e8EGMEKjV+PrgofGW6Kwh9nhh5vrmG/A="',
# "Sec-Fetch-Dest": "document",
# "Sec-Fetch-Mode": "navigate",
# "Sec-Fetch-Site": "same-origin",
# "Sec-Fetch-User": "?1",
# "Sec-GPC": "1",
# "Cache-Control": "max-age=0"
}

def get_request(url: str) -> Optional[bytes]:
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        if r.status_code > 500:
            print("Probably rate-restricted, code " + r.status_code)
        else:
            print("Got error " + r.status_code)
        return None
    else:
        return r.content

def clean_soup(soup: BeautifulSoup) -> BeautifulSoup:
    widget = soup.find(class_="widgetId=loom-desktop-top-slot_hsa-id")
    if widget is not None:
        widget.decompose()
    return soup

def get_all_items(term: str, fields: Dict[str, str]) -> List[Dict[str, str]]:
    
    def get_page_items(page: int):
        r = get_request(search_url(term, page))
        if r is None:
            return []
        soup = clean_soup(BeautifulSoup(r, "lxml"))
        return [x for x in soup.find_all("div", class_="s-result-item") if "AdHolder" not in x["class"] and x.find(class_="a-price-whole") is not None]
    
    page = 1
    page_items = get_page_items(page)
    while len(page_items) != 0:
        page += 1
        page_items = get_page_items(page)


get_all_items("tennis balls", {})    
