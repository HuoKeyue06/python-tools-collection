# 豆瓣电影爬虫

**功能**：采集豆瓣电影TOP250的片名和评分，自动保存为Excel文件。

**使用方法**：
```bash
# 1. 安装依赖（仅首次需要）
pip install requests beautifulsoup4 pandas openpyxl lxml

# 2. 运行脚本
python douban_spider.py
```

**输出结果**：运行后会在当前文件夹生成 `douban_movies.xlsx`。

**技术栈**：`requests` + `BeautifulSoup` + `pandas`

**适用场景**：采集公开的网页列表数据（如商品信息、新闻标题等）。

---
*项目来自我的Python接单作品集*

