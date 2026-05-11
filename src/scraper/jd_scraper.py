"""
京东爬虫实现
"""
from typing import List, Optional
from bs4 import BeautifulSoup
import random
from .base_scraper import BaseScraper
from ..models.product import Product


class JDScraper(BaseScraper):
    """京东爬虫"""

    def __init__(self):
        super().__init__("jd")

    def search_url(self, keyword: str, page: int = 1) -> str:
        """生成京东搜索URL"""
        from urllib.parse import quote
        keyword_encoded = quote(keyword)
        return f"https://search.jd.com/Search?keyword={keyword_encoded}&enc=utf-8&wq={keyword_encoded}&pvid=75f0442f5fad4c6ab3ed1c9b08c2f8c5&page={2 * page - 1}"

    def extract_items(self, soup: BeautifulSoup) -> List:
        """提取京东商品列表"""
        items = soup.select('div.gl-i-wrap')
        if not items:
            items = soup.select('.gl-item')
        if not items:
            items = soup.select('[class*="gl-item"]')
        return items

    def parse_product(self, item) -> Optional[Product]:
        """解析京东商品"""
        try:
            name_elem = item.select_one('.p-name em') or item.select_one('.p-name a') or item.select_one('div.p-name')
            if not name_elem:
                return None

            name = name_elem.get_text(strip=True)

            price_elem = item.select_one('.p-price i') or item.select_one('.p-price strong i') or item.select_one('[class*="price"]')
            price = 0.0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                try:
                    price = float(price_text)
                except:
                    price = 0.0

            sales_elem = item.select_one('.p-commit a') or item.select_one('.p-commit')
            sales = self._parse_sales(sales_elem.get_text() if sales_elem else "")

            rating_elem = item.select_one('.p-commit strong') or item.select_one('[class*="rating"]')
            rating = self._parse_rating(rating_elem.get_text() if rating_elem else "")

            store_elem = item.select_one('.p-shop') or item.select_one('.p-shop a') or item.select_one('[class*="shop"]')
            store = store_elem.get_text(strip=True) if store_elem else ""

            url_elem = item.select_one('.p-name a') or item.select_one('a[href*="jd.com"]')
            url = ""
            if url_elem:
                url = url_elem.get('href', '')
                if url and not url.startswith('http'):
                    url = 'https:' + url

            img_elem = item.select_one('img[data-src]') or item.select_one('img[lazy-img]') or item.select_one('img')
            thumbnail = ""
            if img_elem:
                thumbnail = img_elem.get('data-src') or img_elem.get('src') or img_elem.get('lazy-img', '')

            product_id = f"jd_{abs(hash(name))}"

            return Product(
                id=product_id,
                name=name,
                price=price,
                sales=sales,
                rating=rating,
                platform="jd",
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
