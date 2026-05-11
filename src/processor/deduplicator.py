"""
数据去重引擎
识别和合并重复商品
"""
from typing import List, Set, Dict
from ..models.product import Product
import re


class Deduplicator:
    """商品去重引擎"""

    def __init__(self, similarity_threshold: float = 0.8):
        """
        初始化去重器

        Args:
            similarity_threshold: 相似度阈值,默认0.8(80%)
        """
        self.threshold = similarity_threshold

    def normalize_name(self, name: str) -> str:
        """
        标准化商品名称
        转小写,移除非字母数字字符
        """
        if not name:
            return ""

        name = name.lower()

        name = re.sub(r'[^a-z0-9\u4e00-\u9fa5]', '', name)

        return name

    def calculate_similarity(self, name1: str, name2: str) -> float:
        """
        计算两个名称的相似度
        使用集合交集方法

        Returns:
            0.0 到 1.0 之间的相似度值
        """
        s1 = self.normalize_name(name1)
        s2 = self.normalize_name(name2)

        if not s1 or not s2:
            return 0.0

        if s1 == s2:
            return 1.0

        set1 = set(s1)
        set2 = set(s2)

        common = set1 & set2
        total = set1 | set2

        return len(common) / len(total) if total else 0.0

    def calculate_levenshtein_similarity(self, name1: str, name2: str) -> float:
        """
        使用编辑距离计算相似度
        更精确但计算成本更高
        """
        s1 = self.normalize_name(name1)
        s2 = self.normalize_name(name2)

        if not s1 or not s2:
            return 0.0

        if s1 == s2:
            return 1.0

        len1, len2 = len(s1), len(s2)
        max_len = max(len1, len2)

        if max_len == 0:
            return 1.0

        distance = self._levenshtein_distance(s1, s2)

        return 1.0 - (distance / max_len)

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """计算编辑距离"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def is_duplicate(self, p1: Product, p2: Product) -> bool:
        """
        判断两个商品是否重复

        判断规则:
        1. 完全相同的名称
        2. 名称相似度>=阈值 且 价格相近(差异<20%)
        """
        if not p1.name or not p2.name:
            return False

        if p1.name == p2.name:
            return True

        similarity = self.calculate_similarity(p1.name, p2.name)

        if similarity >= self.threshold:
            if p1.price > 0 and p2.price > 0:
                price_diff = abs(p1.price - p2.price) / max(p1.price, p2.price)
                if price_diff < 0.2:
                    return True

        return False

    def find_duplicates(self, product: Product, product_list: List[Product]) -> List[Product]:
        """查找商品列表中与给定商品重复的所有商品"""
        duplicates = []

        for p in product_list:
            if p.id != product.id and self.is_duplicate(product, p):
                duplicates.append(p)

        return duplicates

    def deduplicate(self, products: List[Product]) -> List[Product]:
        """
        去重处理

        策略:
        1. 遍历每个商品
        2. 如果与已有商品重复,保留质量更好的(评分*销量更高)
        3. 否则加入结果列表
        """
        if not products:
            return []

        unique_products = []

        for product in products:
            is_dup = False

            for i, existing in enumerate(unique_products):
                if self.is_duplicate(product, existing):
                    existing_score = existing.rating * max(existing.sales, 1)
                    new_score = product.rating * max(product.sales, 1)

                    if new_score > existing_score:
                        unique_products[i] = product

                    is_dup = True
                    break

            if not is_dup:
                unique_products.append(product)

        return unique_products

    def deduplicate_with_groups(self, products: List[Product]) -> Dict[int, List[Product]]:
        """
        去重并返回分组信息

        Returns:
            Dict[group_id, List[Product]]
        """
        if not products:
            return {}

        groups = []
        group_ids = {}

        for product in products:
            found_group = False

            for group_id, group in enumerate(groups):
                if self.is_duplicate(product, group[0]):
                    group.append(product)
                    group_ids[id(product)] = group_id
                    found_group = True
                    break

            if not found_group:
                groups.append([product])
                group_ids[id(product)] = len(groups) - 1

        result = {}
        for group_id, group in enumerate(groups):
            result[group_id] = group

        return result

    def get_dedup_statistics(self, original: List[Product], deduplicated: List[Product]) -> Dict:
        """获取去重统计信息"""
        original_count = len(original)
        dedup_count = len(deduplicated)
        removed_count = original_count - dedup_count

        return {
            'original_count': original_count,
            'deduplicated_count': dedup_count,
            'removed_count': removed_count,
            'dedup_rate': (removed_count / original_count * 100) if original_count > 0 else 0
        }
