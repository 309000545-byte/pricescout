"""
数据清洗模块
处理和规范化商品数据
"""
import re
from typing import List, Optional
from ..models.product import Product


class DataCleaner:
    """数据清洗器"""

    @staticmethod
    def clean_price(price_str: str) -> float:
        """
        清洗价格字符串
        提取数字和小数点,返回浮点数
        """
        if not price_str:
            return 0.0

        price_str = str(price_str).strip()

        price_str = re.sub(r'[^\d.]', '', price_str)

        price_str = price_str.lstrip('0').lstrip('.')

        try:
            price = float(price_str)
            return max(0.0, price)
        except (ValueError, AttributeError):
            return 0.0

    @staticmethod
    def clean_sales(sales_str: str) -> int:
        """
        清洗销量字符串
        支持万、亿单位转换
        """
        if not sales_str:
            return 0

        sales_str = str(sales_str).strip().upper()

        multiplier = 1
        if '万' in sales_str:
            multiplier = 10000
            sales_str = sales_str.replace('万', '')
        elif '亿' in sales_str:
            multiplier = 100000000
            sales_str = sales_str.replace('亿', '')

        numbers = re.findall(r'\d+\.?\d*', sales_str)
        if numbers:
            try:
                return int(float(numbers[0]) * multiplier)
            except (ValueError, IndexError):
                return 0

        return 0

    @staticmethod
    def clean_rating(rating_str: str) -> float:
        """
        清洗评分字符串
        支持0-5和0-100两种评分系统
        """
        if not rating_str:
            return 0.0

        numbers = re.findall(r'\d+\.?\d*', str(rating_str))
        if numbers:
            try:
                rating = float(numbers[0])

                if rating > 5:
                    rating = rating / 20

                return min(5.0, max(0.0, rating))
            except (ValueError, IndexError):
                return 0.0

        return 0.0

    @staticmethod
    def clean_name(name: str) -> str:
        """
        清洗商品名称
        移除不必要的特殊字符
        """
        if not name:
            return ""

        name = str(name).strip()

        name = re.sub(r'\s+', ' ', name)

        return name

    @staticmethod
    def clean_url(url: str) -> str:
        """清洗URL"""
        if not url:
            return ""

        url = str(url).strip()

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        return url

    @staticmethod
    def clean_store(store: str) -> str:
        """清洗店铺名称"""
        if not store:
            return ""

        store = str(store).strip()

        store = re.sub(r'\s+', '', store)

        return store

    def clean_product(self, product: Product) -> Product:
        """
        清洗单个商品
        应用所有清洗规则
        """
        product.name = self.clean_name(product.name)
        product.price = self.clean_price(str(product.price))

        if product.original_price:
            product.original_price = self.clean_price(str(product.original_price))

        product.sales = self.clean_sales(str(product.sales))
        product.rating = self.clean_rating(str(product.rating))
        product.url = self.clean_url(product.url)
        product.store = self.clean_store(product.store)

        return product

    def clean_products(self, products: List[Product]) -> List[Product]:
        """
        批量清洗商品
        返回清洗后的商品列表
        """
        cleaned = []
        for product in products:
            if product and product.name:
                cleaned_product = self.clean_product(product)
                if cleaned_product.price > 0:
                    cleaned.append(cleaned_product)

        return cleaned

    def filter_invalid_products(self, products: List[Product]) -> List[Product]:
        """
        过滤无效商品
        移除价格、名称为空或不合法的商品
        """
        valid_products = []

        for product in products:
            is_valid = True

            if not product.name or len(product.name) < 3:
                is_valid = False

            if product.price <= 0:
                is_valid = False

            if product.price > 1000000:
                is_valid = False

            if is_valid:
                valid_products.append(product)

        return valid_products
