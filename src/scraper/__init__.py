"""
爬虫模块
"""
from .base_scraper import BaseScraper
from .jd_scraper import JDScraper
from .taobao_scraper import TaobaoScraper
from .pdd_scraper import PDDScraper

__all__ = ['BaseScraper', 'JDScraper', 'TaobaoScraper', 'PDDScraper']
