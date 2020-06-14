## 基础工具

### python 项目
 - spider 爬虫项目
    - 需使用python3
    - 项目依赖：scrapy pypinyin
抓取中国行政区数据，生成sql文件,抓取方法
 
```cmd
    #安装依赖
    pip install scrapy pypinyin
    # 抓取
    cd python/spider
    scrapy crawl china_city
    # 生成的sql文件在dist/sys_city_data.sql
```