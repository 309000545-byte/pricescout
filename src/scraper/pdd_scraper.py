"""
拼多多爬虫实现
"""
from typing import List, Optional
from bs4 import BeautifulSoup
import random
from .base_scraper import BaseScraper
from ..models.product import Product


class PDDScraper(BaseScraper):
    """拼多多爬虫"""

    def __init__(self):
        super().__init__("pdd")

    def search_url(self, keyword: str, page: int = 1) -> str:
        """生成拼多多搜索URL"""
        from urllib.parse import quote
        keyword_encoded = quote(keyword)
        return f"https://mobile.yangkeduo.com/search_result.html?search_key={keyword_encoded}&page={page}&size=20"

    def extract_items(self, soup: BeautifulSoup) -> List:
        """提取拼多多商品列表"""
        items = soup.select('.goods-item') or soup.select('[class*="goods"]')
        if not items:
            items = soup.select('.search-goods-item')
        if not items:
            items = soup.select('div[data-spm]')
        return items

    def parse_product(self, item) -> Optional[Product]:
        """解析拼多多商品"""
        try:
            name_elem = item.select_one('.goods-name') or item.select_one('.goods-title') or item.select_one('[class*="name"]')
            if not name_elem:
                return None

            name = name_elem.get_text(strip=True)
            if not name or len(name) < 3:
                return None

            price_elem = item.select_one('.goods-price') or item.select_one('.price') or item.select_one('[class*="price"]')
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

            sales_elem = item.select_one('.goods-sales') or item.select_one('[class*="sales"]')
            sales = self._parse_sales(sales_elem.get_text() if sales_elem else "")

            rating = 4.5

            store_elem = item.select_one('.mall-name') or item.select_one('.shop-name') or item.select_one('[class*="mall"]')
            store = ""
            if store_elem:
                store = store_elem.get_text(strip=True)

            url_elem = item.select_one('a[href]')
            url = ""
            if url_elem:
                url = url_elem.get('href', '')
                if url and not url.startswith('http'):
                    url = 'https://mobile.yangkeduo.com' + url

            img_elem = item.select_one('img[data-src]') or item.select_one('img')
            thumbnail = ""
            if img_elem:
                thumbnail = img_elem.get('data-src') or img_elem.get('src', '')

            product_id = f"pdd_{abs(hash(name))}"

            return Product(
                id=product_id,
                name=name,
                price=price,
                sales=sales,
                rating=rating,
                platform="pdd",
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
