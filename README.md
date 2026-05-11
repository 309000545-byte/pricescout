# PriceScout - 智能电商价格采集与对比工具

🛒 采集 · 对比 · 推荐 · 分析

## 📖 项目简介

PriceScout 是一款功能强大的电商商品价格采集与对比工具，支持从京东、淘宝、拼多多等主流电商平台批量抓取商品信息，提供智能去重、价格排序、性价比推荐和数据可视化功能。

## ✨ 核心特性

- 🌐 **多平台支持**: 京东、淘宝、拼多多三大主流电商平台
- 🔍 **批量采集**: 支持关键词搜索，批量抓取商品数据
- 🧹 **智能清洗**: 自动清洗去重，数据规范化处理
- 📊 **价格排序**: 按价格从低到高排序，轻松比价
- 🏆 **性价比推荐**: 基于评分、销量、价格综合计算，智能推荐高性价比商品
- 📈 **可视化分析**: 价格分布图、平台对比图等数据可视化
- 💾 **多格式导出**: 支持 JSON、CSV 格式导出
- 🎨 **网页演示**: 提供交互式网页演示，即开即用

## 🛠️ 技术栈

### 命令行工具
- **Python 3.8+**
- `requests` - HTTP 请求
- `beautifulsoup4` - HTML 解析
- `click` - CLI 框架
- `colorama` - 彩色输出

### 网页演示
- **HTML5 + CSS3 + JavaScript ES6+**
- TailwindCSS 3.0 - 样式框架
- Chart.js 4.0 - 数据可视化
- Font Awesome 6.0 - 图标库

## 📦 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd pricescout
```

### 2. 安装 Python 依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 验证安装

```bash
python cli.py --version
```

## 🚀 快速开始

### 命令行工具

#### 基本搜索

```bash
python cli.py search "无线蓝牙耳机"
```

#### 指定平台

```bash
# 仅搜索京东
python cli.py search "机械键盘" --platform jd

# 搜索淘宝和拼多多
python cli.py search "运动鞋" --platform taobao --platform pdd
```

#### 设置采集页数

```bash
python cli.py search "手机" --pages 5
```

#### 导出结果

```bash
# 导出为 JSON
python cli.py search "笔记本" -o result.json

# 导出为 CSV
python cli.py search "平板" -o result.csv --format csv
```

#### 功能演示

```bash
python cli.py demo
```

#### 查看帮助

```bash
python cli.py info
```

### 网页演示

直接在浏览器中打开 `web-demo.html` 文件即可体验完整功能：

```bash
# Windows
start web-demo.html

# macOS
open web-demo.html

# Linux
xdg-open web-demo.html
```

或直接双击文件打开。

## 📋 功能详情

### 1. 数据采集

工具支持从以下平台采集数据：

| 平台 | 代码 | 特点 |
|------|------|------|
| 京东 | `jd` | 商品丰富，数据准确 |
| 淘宝 | `taobao` | 品牌多样，价格实惠 |
| 拼多多 | `pdd` | 价格低廉，团购优惠 |

### 2. 商品数据字段

采集的商品信息包含：

- **商品名称**: 商品完整名称
- **现价**: 当前售价
- **原价**: 原始标价（如有折扣）
- **销量**: 商品销量
- **评分**: 商品评分（0-5分）
- **店铺**: 店铺名称
- **平台**: 商品来源平台
- **链接**: 商品详情页链接

### 3. 智能分析

- **自动去重**: 基于名称相似度和价格差异智能去重
- **价格排序**: 按价格从低到高排序
- **性价比指数**: `(评分 × 销量) / 价格`，数值越高性价比越好
- **价格分布**: 统计各价格区间的商品数量

### 4. 性价比推荐

系统会根据以下规则推荐高性价比商品：

1. 评分 ≥ 4.0 分
2. 销量 ≥ 1000
3. 按性价比指数从高到低排序

## 📊 使用示例

### 示例 1: 搜索蓝牙耳机

```bash
$ python cli.py search "无线蓝牙耳机" --platform all

🛒 PriceScout - 电商价格采集工具
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 正在采集: 无线蓝牙耳机
  • 京东
  • 淘宝
  • 拼多多

✅ 京东: 找到 45 件商品
✅ 淘宝: 找到 52 件商品
✅ 拼多多: 找到 38 件商品

📊 数据处理完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原始数据: 135 件
去重后:   89 件

📈 统计信息:
  价格区间: ¥29.9 - ¥999.0
  平均价格: ¥189.5
  总销量:   3,424,000
  平均评分: 4.6 ⭐

🏆 性价比 TOP 3 推荐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 【京东】漫步者声迈 X3 真无线蓝牙耳机
   💰 ¥49.9  ⭐ 4.6  📈 15.6万
   🏷️ 性价比指数: 14382.77

2. 【拼多多】漫步者声迈X3蓝牙耳机
   💰 ¥39.9  ⭐ 4.4  📈 45.6万
   🏷️ 性价比指数: 50275.69

3. 【京东】QCY T13 真无线蓝牙耳机
   💰 ¥79.9  ⭐ 4.5  📈 9.8万
   🏷️ 性价比指数: 5513.14
```

### 示例 2: 使用示例数据演示

```bash
$ python cli.py demo
```

这将加载 `sample_data.json` 中的示例数据，展示完整的功能演示。

## 📁 项目结构

```
pricescout/
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖
├── cli.py                 # 命令行工具入口
├── web-demo.html          # 网页演示页面
├── sample_data.json       # 示例数据
│
├── src/                   # 源代码目录
│   ├── __init__.py
│   │
│   ├── models/           # 数据模型
│   │   ├── __init__.py
│   │   └── product.py    # 商品模型
│   │
│   ├── scraper/          # 爬虫模块
│   │   ├── __init__.py
│   │   ├── base_scraper.py    # 爬虫基类
│   │   ├── jd_scraper.py      # 京东爬虫
│   │   ├── taobao_scraper.py  # 淘宝爬虫
│   │   └── pdd_scraper.py     # 拼多多爬虫
│   │
│   ├── processor/        # 数据处理
│   │   ├── __init__.py
│   │   ├── cleaner.py        # 数据清洗
│   │   ├── deduplicator.py   # 去重引擎
│   │   └── analyzer.py       # 分析引擎
│   │
│   └── utils/            # 工具函数
│       ├── __init__.py
│       ├── http_client.py    # HTTP 客户端
│       └── formatters.py     # 格式化工具
│
└── .trae/
    └── documents/        # 文档目录
        ├── PRD.md               # 产品需求文档
        └── Technical-Architecture.md  # 技术架构文档
```

## ⚙️ 配置说明

### 反爬策略

工具内置了以下反爬策略：

- **随机 User-Agent**: 每次请求随机选择 User-Agent
- **请求间隔**: 每次请求间隔 1-3 秒
- **失败重试**: 最多重试 3 次
- **超时处理**: 请求超时 10 秒

### 性能优化

- **并行采集**: 支持多平台并行采集
- **缓存机制**: 可选的内存缓存
- **数据清洗**: 自动过滤无效数据

## ⚠️ 注意事项

1. **法律合规**: 请遵守各平台的 robots.txt 和服务条款
2. **合理使用**: 建议设置合理的请求间隔，避免过度访问
3. **数据准确性**: 示例数据仅供演示，真实数据需要网络连接
4. **更新频率**: 商品价格和销量会实时变化

## 🐛 问题排查

### 常见问题

**Q: 采集失败怎么办？**

A: 检查网络连接，或使用 `--mock` 参数加载示例数据：
```bash
python cli.py search "关键词" --mock
```

**Q: 如何导出数据？**

A: 使用 `-o` 参数指定输出文件：
```bash
python cli.py search "关键词" -o result.json
```

**Q: 网页无法加载数据？**

A: 确保 `web-demo.html` 和 `sample_data.json` 在同一目录下

## 📚 扩展开发

### 添加新平台

1. 在 `src/scraper/` 目录下创建新的爬虫类
2. 继承 `BaseScraper` 类
3. 实现 `search_url()`, `extract_items()`, `parse_product()` 方法
4. 在 `cli.py` 中的 `SCRAPERS` 字典注册新爬虫

### 自定义分析规则

在 `src/processor/analyzer.py` 中修改分析逻辑，或创建新的分析器类。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

- **项目主页**: [GitHub Repository]
- **问题反馈**: [Issue Tracker]

## 🙏 致谢

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [Click](https://click.palletsprojects.com/) - CLI 框架
- [Chart.js](https://www.chartjs.org/) - 数据可视化
- [TailwindCSS](https://tailwindcss.com/) - CSS 框架

---

Made with ❤️ by PriceScout Team
