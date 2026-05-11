"""
PriceScout CLI - 电商商品价格采集与对比工具
命令行入口
"""
import click
import json
import sys
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

from src.models.product import Product, SearchResult
from src.scraper.jd_scraper import JDScraper
from src.scraper.taobao_scraper import TaobaoScraper
from src.scraper.pdd_scraper import PDDScraper
from src.processor.cleaner import DataCleaner
from src.processor.deduplicator import Deduplicator
from src.processor.analyzer import ProductAnalyzer
from src.utils.formatters import DataFormatter

SCRAPERS = {
    'jd': JDScraper,
    'taobao': TaobaoScraper,
    'pdd': PDDScraper
}

PLATFORM_NAMES = {
    'jd': '京东',
    'taobao': '淘宝',
    'pdd': '拼多多'
}


def print_banner():
    """打印工具banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   {Fore.WHITE}🛒 PriceScout - 智能电商价格采集工具{Fore.CYAN}                ║
║                                                          ║
║   {Fore.WHITE}采集 · 对比 · 推荐 · 分析{Fore.CYAN}                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_searching(keyword: str, platforms: list):
    """打印搜索开始信息"""
    print(f"\n{Fore.YELLOW}📦 正在采集: {keyword}")
    print(f"{Fore.CYAN}{'─' * 60}")
    for platform in platforms:
        platform_name = PLATFORM_NAMES.get(platform, platform)
        print(f"  {Fore.WHITE}• {platform_name}", end=" ")
    print(f"\n")


def print_platform_result(platform: str, count: int, success: bool = True):
    """打印平台采集结果"""
    platform_name = PLATFORM_NAMES.get(platform, platform)
    if success:
        print(f"{Fore.GREEN}✅ {platform_name}: 找到 {count} 件商品")
    else:
        print(f"{Fore.RED}❌ {platform_name}: 采集失败")


def print_processing_stats(original_count: int, dedup_count: int):
    """打印数据处理统计"""
    print(f"\n{Fore.CYAN}{'─' * 60}")
    print(f"{Fore.YELLOW}📊 数据处理完成")
    print(f"{Fore.WHITE}   原始数据: {original_count} 件")
    print(f"{Fore.GREEN}   去重后:   {dedup_count} 件")
    removed = original_count - dedup_count
    if removed > 0:
        print(f"{Fore.RED}   重复数据: {removed} 件")


def print_statistics(stats: dict):
    """打印统计信息"""
    if not stats:
        return

    print(f"\n{Fore.YELLOW}📈 统计信息:")
    print(f"{Fore.WHITE}   价格区间: {DataFormatter.format_price(stats['min_price'])} - {DataFormatter.format_price(stats['max_price'])}")
    print(f"{Fore.WHITE}   平均价格: {DataFormatter.format_price(stats['avg_price'])}")
    print(f"{Fore.WHITE}   总销量:   {DataFormatter.format_sales(stats['total_sales'])}")
    print(f"{Fore.WHITE}   平均评分: {stats['avg_rating']:.1f} ⭐")


def print_recommendations(products: list, top_n: int = 3):
    """打印推荐商品"""
    if not products:
        print(f"\n{Fore.YELLOW}🏆 暂无推荐商品")
        return

    print(f"\n{Fore.YELLOW}🏆 性价比 TOP {top_n} 推荐")
    print(f"{Fore.CYAN}{'─' * 60}")

    for i, product in enumerate(products[:top_n], 1):
        platform_name = PLATFORM_NAMES.get(product.platform, product.platform)
        print(f"\n{Fore.CYAN}{i}. 【{platform_name}】{product.name}")
        print(f"   {Fore.GREEN}💰 {DataFormatter.format_price(product.price)}{Fore.WHITE}  ", end="")
        print(f"{Fore.YELLOW}⭐ {product.rating:.1f}  ", end="")
        print(f"{Fore.BLUE}📈 {DataFormatter.format_sales(product.sales)}")
        print(f"   {Fore.MAGENTA}🏷️  性价比指数: {DataFormatter.format_value_score(product.get_value_score())}")


def print_price_distribution(distribution: dict):
    """打印价格分布"""
    if not distribution:
        return

    print(f"\n{Fore.YELLOW}💹 价格分布:")
    print(f"{Fore.WHITE}   ", end="")

    ranges = []
    for range_name, count in distribution.items():
        if count > 0:
            ranges.append(f"{range_name}: {count}件")

    print(" | ".join(ranges))


def print_platform_comparison(comparison: dict):
    """打印平台价格对比"""
    if not comparison:
        return

    print(f"\n{Fore.YELLOW}🏪 平台价格对比:")
    for platform, prices in comparison.items():
        platform_name = PLATFORM_NAMES.get(platform, platform)
        print(f"   {platform_name}: ")
        print(f"      最低: {DataFormatter.format_price(prices['min'])}")
        print(f"      最高: {DataFormatter.format_price(prices['max'])}")
        print(f"      平均: {DataFormatter.format_price(prices['avg'])}")


def print_saved_file(filepath: str):
    """打印文件保存信息"""
    print(f"\n{Fore.GREEN}💾 报告已保存: {filepath}")


def load_sample_data():
    """加载示例数据"""
    try:
        with open('sample_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Fore.RED}加载示例数据失败: {e}")
        return None


def scrape_platform(platform: str, keyword: str, max_pages: int = 3) -> tuple:
    """
    采集单个平台数据

    Returns:
        (platform, products, success)
    """
    try:
        scraper_class = SCRAPERS.get(platform)
        if not scraper_class:
            return (platform, [], False)

        scraper = scraper_class()
        products = scraper.scrape(keyword, max_pages)

        return (platform, products, True)
    except Exception as e:
        print(f"{Fore.RED}采集{platform}失败: {e}")
        return (platform, [], False)


def search_products(keyword: str, platforms: list, max_pages: int = 3, use_mock: bool = False) -> SearchResult:
    """
    搜索商品

    Args:
        keyword: 搜索关键词
        platforms: 平台列表
        max_pages: 最大页数
        use_mock: 是否使用模拟数据

    Returns:
        SearchResult对象
    """
    if use_mock:
        data = load_sample_data()
        if data:
            products = [Product(**p) for p in data['products']]
            result = SearchResult(
                keyword=keyword,
                total=len(products),
                products=products,
                statistics=data['statistics'],
                recommendations=[Product(**r) for r in data.get('recommendations', [])],
                price_distribution=data.get('price_distribution', {})
            )
            return result

    all_products = []

    print_searching(keyword, platforms)

    for platform in platforms:
        platform, products, success = scrape_platform(platform, keyword, max_pages)
        print_platform_result(platform, len(products), success)
        all_products.extend(products)

    cleaner = DataCleaner()
    all_products = cleaner.clean_products(all_products)

    print_processing_stats(len(all_products), len(all_products))

    deduplicator = Deduplicator()
    unique_products = deduplicator.deduplicate(all_products)

    if len(all_products) != len(unique_products):
        print_processing_stats(len(all_products), len(unique_products))

    analyzer = ProductAnalyzer()
    sorted_products = analyzer.sort_by_price(unique_products)
    recommendations = analyzer.get_top_recommendations(unique_products, 3)
    statistics = analyzer.calculate_statistics(unique_products)
    price_distribution = analyzer.price_distribution(unique_products)
    platform_comparison = analyzer.price_comparison(unique_products)

    print_statistics(statistics)
    print_price_distribution(price_distribution)
    print_platform_comparison(platform_comparison)
    print_recommendations(recommendations)

    return SearchResult(
        keyword=keyword,
        total=len(unique_products),
        products=sorted_products,
        statistics=statistics,
        recommendations=recommendations,
        price_distribution=price_distribution
    )


def export_results(result: SearchResult, output_path: str, format: str = 'json'):
    """
    导出结果

    Args:
        result: 搜索结果
        output_path: 输出路径
        format: 输出格式(json/csv)
    """
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
    elif format == 'csv':
        import csv
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            if result.products:
                fieldnames = ['平台', '商品名称', '价格', '销量', '评分', '店铺', '性价比', '链接']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for product in result.products:
                    row = {
                        '平台': PLATFORM_NAMES.get(product.platform, product.platform),
                        '商品名称': product.name,
                        '价格': f"{product.price:.2f}",
                        '销量': product.format_sales(),
                        '评分': f"{product.rating:.1f}",
                        '店铺': product.store,
                        '性价比': f"{product.get_value_score():.2f}",
                        '链接': product.url
                    }
                    writer.writerow(row)

    print_saved_file(output_path)


@click.group()
@click.version_option(version='1.0.0', prog_name='PriceScout')
def cli():
    """PriceScout - 智能电商价格采集与对比工具"""
    pass


@cli.command()
@click.argument('keyword', type=str)
@click.option('--platform', '-p', type=click.Choice(['jd', 'taobao', 'pdd', 'all']),
              default='all', help='选择电商平台')
@click.option('--pages', type=int, default=3, help='采集页数')
@click.option('--output', '-o', type=str, help='输出文件路径')
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json',
              help='输出格式')
@click.option('--mock', is_flag=True, help='使用示例数据进行演示')
def search(keyword, platform, pages, output, format, mock):
    """搜索商品并采集价格信息"""
    print_banner()

    if platform == 'all':
        platforms = ['jd', 'taobao', 'pdd']
    else:
        platforms = [platform]

    result = search_products(keyword, platforms, pages, use_mock=mock)

    if output:
        export_results(result, output, format)


@cli.command()
def demo():
    """展示示例数据和功能演示"""
    print_banner()

    print(f"{Fore.YELLOW}📊 加载示例数据...")

    result = search_products("无线蓝牙耳机", ['jd', 'taobao', 'pdd'], use_mock=True)

    print(f"\n{Fore.GREEN}✅ 演示完成!")
    print(f"{Fore.WHITE}如需采集真实数据,请使用:")
    print(f"{Fore.CYAN}  pricescout search \"关键词\" --platform all")


@cli.command()
def info():
    """显示工具信息和帮助"""
    print_banner()

    info_text = f"""
{Fore.YELLOW}🔧 功能特性:
{Fore.WHITE}  • 支持京东、淘宝、拼多多三大平台
  • 自动清洗和去重商品数据
  • 按价格排序,智能推荐性价比商品
  • 支持JSON和CSV格式导出
  • 提供价格分布和平台对比分析

{Fore.YELLOW}📖 使用方法:
{Fore.WHITE}  1. 基本搜索:
{Fore.CYAN}     pricescout search \"关键词\"
{Fore.WHITE}  2. 指定平台:
{Fore.CYAN}     pricescout search \"关键词\" --platform jd
{Fore.WHITE}  3. 设置页数:
{Fore.CYAN}     pricescout search \"关键词\" --pages 5
{Fore.WHITE}  4. 导出结果:
{Fore.CYAN}     pricescout search \"关键词\" -o result.json
{Fore.WHITE}  5. CSV格式:
{Fore.CYAN}     pricescout search \"关键词\" -o result.csv --format csv
{Fore.WHITE}  6. 功能演示:
{Fore.CYAN}     pricescout demo

{Fore.YELLOW}⚠️  注意事项:
{Fore.WHITE}  • 请遵守各平台的robots.txt和服务条款
  • 建议设置合理的请求间隔,避免过度访问
  • 示例数据仅供演示,真实数据需要网络连接
"""
    print(info_text)


if __name__ == '__main__':
    cli()
