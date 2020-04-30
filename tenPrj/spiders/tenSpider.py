# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tenPrj.items import TenprjItem
from selenium import webdriver


class TenspiderSpider(CrawlSpider):
    name = 'tenSpider'
    allowed_domains = ['www.foreverblog.cn']
    start_urls = ['https://www.foreverblog.cn/blogs.html']
    def __init__(self):
        self.browser = webdriver.Chrome("D:\program\chromedriver.exe")
        self.browser.set_page_load_timeout(30)


    rules = (
        Rule(LinkExtractor(allow=r'.+blog.+\.html'), callback="parse_item", follow=False),
    )



    def parse_item(self, response):
        title = response.xpath("//div[@class='cleft']/h2/text()").get()
        words = response.xpath("//div[@class='cleft']/p/text()").get()
        img = response.xpath("//div[@class='cleft']/img/@src").get()
        url = response.xpath("//div[@class='cleft']//a/@href").get()

        words = words.split(": ")[1]
        item = TenprjItem(title=title, words=words, img=img,url=url)
        yield item
