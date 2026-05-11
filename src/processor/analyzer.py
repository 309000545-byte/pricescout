"""
商品分析引擎
提供数据分析和统计功能
"""
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from ..models.product import Product


class ProductAnalyzer:
    """商品分析引擎"""

    @staticmethod
    def sort_by_price(products: List[Product], ascending: bool = True) -> List[Product]:
        """
        按价格排序

        Args:
            products: 商品列表
            ascending: True为升序,False为降序

        Returns:
            排序后的商品列表
        """
        return sorted(
            products,
            key=lambda p: p.price if p.price else float('inf'),
            reverse=not ascending
        )

    @staticmethod
    def sort_by_sales(products: List[Product], ascending: bool = False) -> List[Product]:
        """按销量排序"""
        return sorted(
            products,
            key=lambda p: p.sales,
            reverse=not ascending
        )

    @staticmethod
    def sort_by_rating(products: List[Product], ascending: bool = False) -> List[Product]:
        """按评分排序"""
        return sorted(
            products,
            key=lambda p: p.rating,
            reverse=not ascending
        )

    @staticmethod
    def sort_by_value_score(products: List[Product], ascending: bool = False) -> List[Product]:
        """按性价比排序"""
        return sorted(
            products,
            key=lambda p: p.get_value_score(),
            reverse=not ascending
        )

    @staticmethod
    def filter_by_price_range(
        products: List[Product],
        min_price: float = 0,
        max_price: float = float('inf')
    ) -> List[Product]:
        """
        按价格区间筛选

        Args:
            min_price: 最低价格
            max_price: 最高价格

        Returns:
            筛选后的商品列表
        """
        return [
            p for p in products
            if min_price <= (p.price or 0) <= max_price
        ]

    @staticmethod
    def filter_by_platform(products: List[Product], platform: str) -> List[Product]:
        """按平台筛选"""
        return [p for p in products if p.platform == platform]

    @staticmethod
    def calculate_statistics(products: List[Product]) -> Dict[str, Any]:
        """
        计算统计信息

        Returns:
            包含各种统计指标的字典
        """
        if not products:
            return {
                'count': 0,
                'min_price': 0,
                'max_price': 0,
                'avg_price': 0,
                'median_price': 0,
                'total_sales': 0,
                'avg_sales': 0,
                'avg_rating': 0
            }

        prices = [p.price for p in products if p.price > 0]
        sales = [p.sales for p in products if p.sales > 0]
        ratings = [p.rating for p in products if p.rating > 0]

        prices.sort()
        median_price = prices[len(prices) // 2] if prices else 0

        return {
            'count': len(products),
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'median_price': median_price,
            'total_sales': sum(sales) if sales else 0,
            'avg_sales': sum(sales) / len(sales) if sales else 0,
            'avg_rating': sum(ratings) / len(ratings) if ratings else 0
        }

    @staticmethod
    def group_by_platform(products: List[Product]) -> Dict[str, List[Product]]:
        """按平台分组"""
        groups = defaultdict(list)
        for p in products:
            groups[p.platform].append(p)
        return dict(groups)

    @staticmethod
    def get_platform_statistics(products: List[Product]) -> Dict[str, Dict[str, Any]]:
        """获取各平台统计信息"""
        groups = ProductAnalyzer.group_by_platform(products)

        platform_stats = {}
        for platform, platform_products in groups.items():
            stats = ProductAnalyzer.calculate_statistics(platform_products)
            platform_stats[platform] = stats

        return platform_stats

    @staticmethod
    def get_top_recommendations(
        products: List[Product],
        top_n: int = 5,
        min_rating: float = 4.0,
        min_sales: int = 1000
    ) -> List[Product]:
        """
        获取性价比TOP推荐

        筛选条件:
        - 评分>=min_rating
        - 销量>=min_sales
        - 按性价比指数排序

        Returns:
            推荐商品列表
        """
        filtered = [
            p for p in products
            if p.rating >= min_rating and p.sales >= min_sales
        ]

        for p in filtered:
            p.value_score = p.get_value_score()

        return sorted(filtered, key=lambda p: p.value_score, reverse=True)[:top_n]

    @staticmethod
    def price_distribution(products: List[Product]) -> Dict[str, int]:
        """
        计算价格区间分布

        Returns:
            各价格区间的商品数量
        """
        distribution = {
            '0-100': 0,
            '100-300': 0,
            '300-500': 0,
            '500-1000': 0,
            '1000+': 0
        }

        for p in products:
            price = p.price or 0
            if price < 100:
                distribution['0-100'] += 1
            elif price < 300:
                distribution['100-300'] += 1
            elif price < 500:
                distribution['300-500'] += 1
            elif price < 1000:
                distribution['500-1000'] += 1
            else:
                distribution['1000+'] += 1

        return distribution

    @staticmethod
    def platform_distribution(products: List[Product]) -> Dict[str, int]:
        """获取平台分布"""
        distribution = defaultdict(int)
        for p in products:
            distribution[p.platform] += 1
        return dict(distribution)

    @staticmethod
    def price_comparison(products: List[Product]) -> Dict[str, Dict[str, float]]:
        """各平台价格对比"""
        groups = ProductAnalyzer.group_by_platform(products)

        comparison = {}
        for platform, platform_products in groups.items():
            prices = [p.price for p in platform_products if p.price > 0]
            if prices:
                comparison[platform] = {
                    'min': min(prices),
                    'max': max(prices),
                    'avg': sum(prices) / len(prices)
                }

        return comparison

    @staticmethod
    def generate_report(products: List[Product]) -> Dict[str, Any]:
        """
        生成完整分析报告

        Returns:
            包含所有分析结果的字典
        """
        if not products:
            return {
                'statistics': {},
                'platforms': {},
                'recommendations': [],
                'price_distribution': {},
                'sorted_by_price': []
            }

        sorted_products = ProductAnalyzer.sort_by_price(products)

        return {
            'statistics': ProductAnalyzer.calculate_statistics(products),
            'platforms': ProductAnalyzer.get_platform_statistics(products),
            'recommendations': ProductAnalyzer.get_top_recommendations(products, 3),
            'price_distribution': ProductAnalyzer.price_distribution(products),
            'platform_distribution': ProductAnalyzer.platform_distribution(products),
            'price_comparison': ProductAnalyzer.price_comparison(products),
            'sorted_by_price': sorted_products
        }

    @staticmethod
    def get_budget_recommendations(
        products: List[Product],
        budget: float
    ) -> Dict[str, List[Product]]:
        """
        根据预算推荐商品

        Args:
            budget: 预算金额

        Returns:
            不同价格区间的推荐商品
        """
        recommendations = {
            'under_budget': [],
            'at_budget': [],
            'above_budget': []
        }

        for p in products:
            if p.price <= budget * 0.8:
                recommendations['under_budget'].append(p)
            elif p.price <= budget:
                recommendations['at_budget'].append(p)
            else:
                recommendations['above_budget'].append(p)

        for key in recommendations:
            recommendations[key] = ProductAnalyzer.sort_by_value_score(
                recommendations[key][:10]
            )

        return recommendations
