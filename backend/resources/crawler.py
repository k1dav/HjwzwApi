"""黃金屋的爬蟲"""
import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://tw.hjwzw.com"
MOBILE_URL = "https://t.hjwzw.com"


async def search_title(title: str) -> list:
    """取得搜尋資料"""
    url = f"{BASE_URL}/List/{title}"

    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return "Error"  # 網站不正常

    soup = BeautifulSoup(res.text, "html.parser")

    # 是直接搜到書本主頁嗎
    main = soup.find_all("a", string=re.compile(f"{title}"))
    is_main = main != None and all([main[0]["href"] in i["href"] for i in main])

    if is_main:
        main = main[0]
        list_ = await get_book_info(main.text.strip(), main["href"])
    else:
        books = soup.find_all("span", class_="wd10")
        list_ = await asyncio.gather(
            *[get_book_info(i.a.text, i.a["href"]) for i in books]
        )
    return list_
