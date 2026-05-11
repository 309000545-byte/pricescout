"""
爬虫基类
提供通用的爬虫功能
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import time
import random
from ..models.product import Product


class BaseScraper(ABC):
    """爬虫基类"""

    def __init__(self, platform: str):
        self.platform = platform
        self.headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        ]
        self.session = requests.Session()
        self.request_count = 0

    def _get_random_headers(self) -> dict:
        """获取随机请求头"""
        return random.choice(self.headers_list).copy()

    def fetch_page(self, url: str, retry: int = 3) -> Optional[str]:
        """
        获取页面内容
        带重试机制和请求间隔
        """
        for attempt in range(retry):
            try:
                headers = self._get_random_headers()
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=10,
                    allow_redirects=True
                )
                response.raise_for_status()

                self.request_count += 1

                if self.request_count > 1:
                    time.sleep(random.uniform(1, 3))

                return response.text

            except requests.exceptions.RequestException as e:
                print(f"请求失败 (尝试 {attempt + 1}/{retry}): {e}")
                if attempt < retry - 1:
                    time.sleep(random.uniform(2, 5))
                continue

        return None

    @abstractmethod
    def search_url(self, keyword: str, page: int = 1) -> str:
        """生成搜索URL"""
        pass

    @abstractmethod
    def extract_items(self, soup: BeautifulSoup):
        """提取商品列表"""
        pass

    @abstractmethod
    def parse_product(self, item) -> Optional[Product]:
        """解析单个商品"""
        pass

    def scrape(self, keyword: str, max_pages: int = 3) -> List[Product]:
        """
        采集商品
        返回商品列表
        """
        all_products = []

        for page in range(1, max_pages + 1):
            url = self.search_url(keyword, page)
            html = self.fetch_page(url)

            if not html:
                continue

            soup = BeautifulSoup(html, 'lxml')
            items = self.extract_items(soup)

            for item in items:
                product = self.parse_product(item)
                if product:
                    all_products.append(product)

        return all_products

    def get_product_count(self, keyword: str) -> int:
        """获取商品总数"""
        html = self.fetch_page(self.search_url(keyword, 1))
        if html:
            soup = BeautifulSoup(html, 'lxml')
            count_text = self._extract_total_count(soup)
            if count_text:
                return self._parse_count(count_text)
        return 0

    def _extract_total_count(self, soup: BeautifulSoup) -> Optional[str]:
        """提取总数量文本"""
        return None

    def _parse_count(self, count_text: str) -> int:
        """解析数量文本"""
        import re
        numbers = re.findall(r'\d+', count_text)
        if numbers:
            return int(numbers[0])
        return 0
