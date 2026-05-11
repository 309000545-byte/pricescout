"""
淘宝爬虫实现
"""
from typing import List, Optional
from bs4 import BeautifulSoup
import random
from .base_scraper import BaseScraper
from ..models.product import Product


class TaobaoScraper(BaseScraper):
    """淘宝爬虫"""

    def __init__(self):
        super().__init__("taobao")

    def search_url(self, keyword: str, page: int = 1) -> str:
        """生成淘宝搜索URL"""
        from urllib.parse import quote
        keyword_encoded = quote(keyword)
        return f"https://s.taobao.com/search?q={keyword_encoded}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{page}&ie=utf8"

    def extract_items(self, soup: BeautifulSoup) -> List:
        """提取淘宝商品列表"""
        items = soup.select('.item')
        if not items:
            items = soup.select('[class*="item"]')
        if not items:
            items = soup.select('.ctx-box')
        return items

    def parse_product(self, item) -> Optional[Product]:
        """解析淘宝商品"""
        try:
            name_elem = item.select_one('.title') or item.select_one('.row-gg')
            if not name_elem:
                name_elem = item.select_one('[class*="title"]')

            if not name_elem:
                return None

            name = name_elem.get_text(strip=True)
            if not name or len(name) < 3:
                return None

            price_elem = item.select_one('.price') or item.select_one('.row-gg')
            price = 0.0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                import re
                numbers = re.findall(r'\d+\.?\d*', price_text)
                if numbers:
                    try:
                        price = float(numbers[0])
                    except:
                        price = 0.0

            sales_elem = item.select_one('.deal-cnt') or item.select_one('[class*="deal"]')
            sales = self._parse_sales(sales_elem.get_text() if sales_elem else "")

            rating_elem = item.select_one('.rate-num') or item.select_one('[class*="rate"]')
            rating = self._parse_rating(rating_elem.get_text() if rating_elem else "")

            store_elem = item.select_one('.shop') or item.select_one('.shopLink') or item.select_one('[class*="shop"]')
            store = ""
            if store_elem:
                store = store_elem.get_text(strip=True)

            url_elem = item.select_one('a[href*="taobao.com"]') or item.select_one('a[href*="tmall.com"]')
            url = ""
            if url_elem:
                url = url_elem.get('href', '')
                if url and not url.startswith('http'):
                    url = 'https:' + url

            img_elem = item.select_one('img[data-src]') or item.select_one('img')
            thumbnail = ""
            if img_elem:
                thumbnail = img_elem.get('data-src') or img_elem.get('src', '')

            product_id = f"taobao_{abs(hash(name))}"

            return Product(
                id=product_id,
                name=name,
                price=price,
                sales=sales,
                rating=rating,
                platform="taobao",
                store=store,
                url=url,
                thumbnail=thumbnail
            )

        except Exception as e:
            return None

    def _parse_sales(self, sales_text: str) -> int:
        """解析销量"""
        import re
        if not sales_text:
            return 0

        sales_text = sales_text.upper()
        multiplier = 1

        if '万' in sales_text:
            multiplier = 10000
            sales_text = sales_text.replace('万', '')
        elif '亿' in sales_text:
            multiplier = 100000000
            sales_text = sales_text.replace('亿', '')

        numbers = re.findall(r'\d+\.?\d*', sales_text)
        if numbers:
            try:
                return int(float(numbers[0]) * multiplier)
            except:
                return 0

        return 0

    def _parse_rating(self, rating_text: str) -> float:
        """解析评分"""
        import re
        if not rating_text:
            return 0.0

        numbers = re.findall(r'\d+\.?\d*', rating_text)
        if numbers:
            try:
                rating = float(numbers[0])
                if rating > 5:
                    rating = rating / 20
                return min(5.0, max(0.0, rating))
            except:
                return 0.0

        return 0.0
