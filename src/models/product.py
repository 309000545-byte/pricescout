"""
商品数据模型
"""
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class Platform(Enum):
    """电商平台枚举"""
    JD = "jd"
    TAOBAO = "taobao"
    PDD = "pdd"

    @classmethod
    def get_name(cls, value: str) -> str:
        """获取平台中文名称"""
        names = {
            "jd": "京东",
            "taobao": "淘宝",
            "pdd": "拼多多"
        }
        return names.get(value, value)


@dataclass
class Product:
    """商品数据模型"""

    id: str = ""
    name: str = ""
    price: float = 0.0
    original_price: Optional[float] = None
    sales: int = 0
    rating: float = 0.0
    platform: str = ""
    store: str = ""
    url: str = ""
    thumbnail: str = ""
    scraped_at: str = ""

    def __post_init__(self):
        """初始化后处理"""
        if not self.scraped_at:
            self.scraped_at = datetime.now().isoformat()
        if not self.id:
            self.id = f"{self.platform}_{abs(hash(self.name))}"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    def get_value_score(self) -> float:
        """
        计算性价比指数
        公式: (评分 * 销量) / 价格
        """
        if self.price <= 0:
            return 0
        return (self.rating * max(self.sales, 1)) / self.price

    def get_platform_name(self) -> str:
        """获取平台中文名称"""
        return Platform.get_name(self.platform)

    def get_discount(self) -> Optional[float]:
        """计算折扣率"""
        if self.original_price and self.original_price > 0:
            return (1 - self.price / self.original_price) * 100
        return None

    def format_sales(self) -> str:
        """格式化销量显示"""
        if self.sales >= 100000000:
            return f"{self.sales / 100000000:.1f}亿"
        elif self.sales >= 10000:
            return f"{self.sales / 10000:.1f}万"
        return str(self.sales)

    def is_recommended(self, threshold: float = 50.0) -> bool:
        """判断是否为推荐商品"""
        return self.get_value_score() >= threshold

    def to_table_row(self) -> Dict[str, str]:
        """转换为表格行数据"""
        return {
            "平台": self.get_platform_name(),
            "商品名称": self.name[:30] + "..." if len(self.name) > 30 else self.name,
            "价格": f"¥{self.price:.2f}",
            "销量": self.format_sales(),
            "评分": f"⭐ {self.rating:.1f}",
            "店铺": self.store[:15] + "..." if len(self.store) > 15 else self.store,
            "链接": self.url[:50] + "..." if len(self.url) > 50 else self.url
        }


@dataclass
class SearchConfig:
    """搜索配置"""
    keyword: str
    platforms: list = field(default_factory=lambda: ["jd", "taobao", "pdd"])
    max_pages: int = 3
    max_products: int = 100


@dataclass
class SearchResult:
    """搜索结果"""
    keyword: str
    total: int = 0
    products: list = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    recommendations: list = field(default_factory=list)
    price_distribution: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "keyword": self.keyword,
            "total": self.total,
            "products": [p.to_dict() if isinstance(p, Product) else p for p in self.products],
            "statistics": self.statistics,
            "recommendations": [r.to_dict() if isinstance(r, Product) else r for r in self.recommendations],
            "price_distribution": self.price_distribution,
            "timestamp": datetime.now().isoformat()
        }
