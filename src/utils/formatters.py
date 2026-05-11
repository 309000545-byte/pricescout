"""
数据格式化工具
提供各种数据格式转换和显示格式化
"""
from typing import List, Dict, Any
from ..models.product import Product


class DataFormatter:
    """数据格式化工具"""

    @staticmethod
    def format_price(price: float, currency: str = "¥") -> str:
        """
        格式化价格

        Args:
            price: 价格数值
            currency: 货币符号

        Returns:
            格式化后的价格字符串
        """
        if price >= 10000:
            return f"{currency}{price:,.2f}"
        return f"{currency}{price:.2f}"

    @staticmethod
    def format_sales(sales: int) -> str:
        """
        格式化销量

        Args:
            sales: 销量数值

        Returns:
            格式化后的销量字符串
        """
        if sales >= 100000000:
            return f"{sales / 100000000:.1f}亿"
        elif sales >= 10000:
            return f"{sales / 10000:.1f}万"
        elif sales >= 1000:
            return f"{sales / 1000:.1f}千"
        return str(sales)

    @staticmethod
    def format_rating(rating: float) -> str:
        """
        格式化评分

        Args:
            rating: 评分数值

        Returns:
            格式化后的评分字符串
        """
        if rating == 0:
            return "暂无评分"
        return f"⭐ {rating:.1f}"

    @staticmethod
    def format_discount(original: float, current: float) -> str:
        """
        格式化折扣

        Args:
            original: 原价
            current: 现价

        Returns:
            折扣信息字符串
        """
        if original <= 0 or current <= 0:
            return ""

        discount = (1 - current / original) * 100

        if discount > 0:
            return f"折扣: {discount:.0f}%"
        return ""

    @staticmethod
    def format_platform(platform: str) -> str:
        """
        格式化平台名称

        Args:
            platform: 平台代码

        Returns:
            平台中文名称
        """
        names = {
            "jd": "京东",
            "taobao": "淘宝",
            "pdd": "拼多多"
        }
        return names.get(platform, platform)

    @staticmethod
    def format_value_score(score: float) -> str:
        """
        格式化性价比指数

        Args:
            score: 性价比指数

        Returns:
            格式化后的性价比指数
        """
        if score >= 100:
            return f"{score:.0f}"
        elif score >= 10:
            return f"{score:.1f}"
        return f"{score:.2f}"

    @staticmethod
    def truncate_text(text: str, max_length: int = 30, suffix: str = "...") -> str:
        """
        截断文本

        Args:
            text: 原文本
            max_length: 最大长度
            suffix: 截断后缀

        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def format_product_summary(product: Product) -> str:
        """
        格式化商品摘要

        Args:
            product: 商品对象

        Returns:
            格式化后的摘要字符串
        """
        lines = [
            f"【{DataFormatter.format_platform(product.platform)}】{product.name}",
            f"价格: {DataFormatter.format_price(product.price)}",
            f"销量: {DataFormatter.format_sales(product.sales)}",
            f"评分: {DataFormatter.format_rating(product.rating)}",
            f"店铺: {product.store}",
            f"性价比: {DataFormatter.format_value_score(product.get_value_score())}"
        ]
        return "\n".join(lines)

    @staticmethod
    def products_to_table_rows(products: List[Product]) -> List[Dict[str, str]]:
        """
        将商品列表转换为表格行

        Args:
            products: 商品列表

        Returns:
            表格行列表
        """
        rows = []
        for i, p in enumerate(products, 1):
            rows.append({
                '序号': str(i),
                '平台': DataFormatter.format_platform(p.platform),
                '商品名称': DataFormatter.truncate_text(p.name, 40),
                '价格': DataFormatter.format_price(p.price),
                '销量': DataFormatter.format_sales(p.sales),
                '评分': DataFormatter.format_rating(p.rating),
                '店铺': DataFormatter.truncate_text(p.store, 15),
                '性价比': DataFormatter.format_value_score(p.get_value_score())
            })
        return rows

    @staticmethod
    def statistics_to_text(stats: Dict[str, Any]) -> str:
        """
        将统计信息转换为文本

        Args:
            stats: 统计信息字典

        Returns:
            格式化后的文本
        """
        if not stats:
            return "暂无统计数据"

        lines = [
            f"商品总数: {stats.get('count', 0)}",
            f"价格范围: {DataFormatter.format_price(stats.get('min_price', 0))} - {DataFormatter.format_price(stats.get('max_price', 0))}",
            f"平均价格: {DataFormatter.format_price(stats.get('avg_price', 0))}",
            f"总销量: {DataFormatter.format_sales(stats.get('total_sales', 0))}",
            f"平均评分: {stats.get('avg_rating', 0):.1f}"
        ]
        return "\n".join(lines)

    @staticmethod
    def format_json(data: Any, indent: int = 2) -> str:
        """
        格式化JSON输出

        Args:
            data: 数据对象
            indent: 缩进空格数

        Returns:
            格式化后的JSON字符串
        """
        import json
        return json.dumps(data, indent=indent, ensure_ascii=False)
