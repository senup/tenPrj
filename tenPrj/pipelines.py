# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



from scrapy.exporters import JsonLinesItemExporter

class TenprjPipeline(object):
    def __init__(self):  # 初始化方法
        # 使用二进制来写入，因此“w”-->"wb"
        self.fp = open("bolg.json", "wb")
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        # self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        print("爬虫开始了！")

    def close_spider(self, spider):
        # self.exporter.finish_exporting()
        self.fp.close()
        print("爬虫结束了！")