# -*- coding: utf-8 -*-
import scrapy
import os
from pypinyin import lazy_pinyin


# 中国行政区 http://www.mca.gov.cn/article/sj/xzqh/2020/

class ChinaCitySpider(scrapy.Spider):
    name = 'china_city'
    allowed_domains = ['www.mca.gov.cn']
    start_urls = ['http://www.mca.gov.cn/article/sj/xzqh/2020/2020/202003301019.html']

    def parse(self, response):
        outPath = '../../dist/'
        outFile = 'sys_city_data.sql'
        table = response.xpath("//table")
        trs = table.xpath("tr")
        list = []
        lastProvinceId = 0
        lastCityId = 0
        for tr in trs:
            code = tr.xpath("td[2]//text()").get()
            nameArr = tr.xpath("td[3]").xpath('string(.)').extract()
            if nameArr and len(nameArr) > 0:
                name = nameArr[0]
                name = name.replace('\xa0', '')
                name = name.strip()
                if code and code.isdigit():
                    code = int(code)
                    if code % 10000 == 0:
                        # 省
                        list.append({'id': code, 'parent_id': 1, 'name': name})
                        if name in ['北京市', '天津市', '上海市', '重庆市']:
                            list.append({'id': code + 100, 'parent_id': code, 'name': name})
                            lastCityId = code + 100
                        lastProvinceId = code
                    elif code % 100 == 0:
                        # 市
                        list.append({'id': code, 'parent_id': lastProvinceId, 'name': name})
                        lastCityId = code
                    else:
                        # 区
                        list.append({'id': code, 'parent_id': lastCityId, 'name': name})
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        out = open(outPath+"/"+outFile, "w", encoding='utf8')
        outStr = ''
        for item in list:
            id = str(item["id"])
            parent_id = str(item["parent_id"])
            name = item["name"]
            spell = " ".join(lazy_pinyin(name))
            outStr += "INSERT INTO `sys_city`(`id`, `parent_id`, `name`, `spell`, `weight`, `data_status`) VALUES (" + id + "," + parent_id + ", '" + name + "', '" + spell + "', 1, 1);\n"
        print(outStr)
        out.write(outStr)
        out.flush()
        out.close()
        pass