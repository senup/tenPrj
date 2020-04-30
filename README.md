晚上在博客汇总页浏览，发觉【[十年之约](https://www.foreverblog.cn/blogs.html)】成员页设计的很不合理。成员页浏览博客需要进入二级页面才能到达博客地址，多次跳转用户体验很不好。于是我想到能不能把这些链接拿下来，或者自己甚至能够仿一个页面，实现点击头像直接到博客真实页面？

于是就有了以下通过scrapy来实现爬虫的经历。

<!--more-->

# 思路

爬取的内容有

- 头像链接
- 博主名称
- 博主寄语
- 网站链接

然后爬取组装成json文件，再用python对该文件进行处理，拼接成html页面。

实现每个人显示头像，点击头像跳转博客，悬浮显示博主寄语的功能。

# 网页分析

一开始分析汇总页，如下

![汇总页](https://img.senup.cn/blog/20200430/C7RR7zHLnSPs.png?imageslim)

然而这里有个最重要的缺点就是：并没有博客的真实地址。

那么也就是说：不得不进入二级页面爬取。

![mark](https://img.senup.cn/blog/20200430/BrSYQx3eW7Vz.png?imageslim)

# 实现

由于之前看过scrapy的爬虫工具书，就动手写写自己比较熟悉的crawlSpider。

## 创建工程

`scrapy startproject tenPrj`

## 创建爬虫

`cd tenPrj`

`scrapy genspider -t crawl tenSpider  www.foreverblog.cn`

## 导入pycharm后

![mark](https://img.senup.cn/blog/20200430/CULqJzcC3TC9.png?imageslim)

习惯性先开启设置三大项

````ini 配置文件setting.py
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
ITEM_PIPELINES = {
   'tenPrj.pipelines.TenprjPipeline': 300,
}
````

编写爬虫文件

````python 编写爬虫文件
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tenPrj.items import TenprjItem

class TenspiderSpider(CrawlSpider):
    name = 'tenSpider'
    allowed_domains = ['www.foreverblog.cn']
    start_urls = ['https://www.foreverblog.cn/blogs.html']

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

````

管道文件

```python pipelines.py
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
```

为了不每次都在cmd控制台输入命令，写一个可以在pycharm多次运行的脚本。

````python start.py
from scrapy import cmdline

cmdline.execute("scrapy crawl tenSpider".split())

````

那么现在运行上面的start.py，

侧栏就会生成一个json文件

````json blog.json
{"title": "胡家小子", "words": "博观而约取，厚积而薄发，十年后遇见一个不一样的自己，回首时间，回首记忆，一切或许也就值得。", "img": "http://cn.gravatar.com/avatar/cbe0cd5bb4c502fdf5a18180a2e2fb35?s=96&d=mp&r=g", "url": "https://boyhu.cn/"}
{"title": "西枫里博客", "words": "坚持所不能坚持的，做个半路的和尚，直到远去。", "img": "http://cn.gravatar.com/avatar/9b0184896389054a6fe867e11cb7ebfb?s=96&d=mp&r=g", "url": "https://www.anji66.net"}
{"title": "比格易尔", "words": "和自己约定个十年，加油！", "img": "https://q2.qlogo.cn/headimg_dl?dst_uin=349778537&spec=100", "url": "https://www.bigeyier.cn"}
{"title": "冰峰博客", "words": "哈哈，静候建国100周年，从头再来", "img": "http://cn.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=96&d=mp&r=g", "url": "https://www.ad-s.cn"}
{"title": "Yuuki的小窝", "words": "不知十年后会怎样。", "img": "https://q2.qlogo.cn/headimg_dl?dst_uin=321124376&spec=100", "url": "http://www.yuukis.cn"}
{"title": "汀彵の汐", "words": "十年之后，我也很想知道，不见不散。", "img": "https://q2.qlogo.cn/headimg_dl?dst_uin=2461306899&spec=100", "url": "https://www.izznan.cn/"}
{"title": "启福", "words": "寥寥数语，皆我心之所慨……\nn年后，我还会在这个遥远而又咫尺的网络世界里~", "img": "http://cn.gravatar.com/avatar/b62a214453c2836a7365803b19eef8c2?s=96&d=mp&r=g", "url": "https://qifu.me/"}
{"title": "喃懂妳", "words": "只希望自己能坚持", "img": "https://q2.qlogo.cn/headimg_dl?dst_uin=249345157&spec=100", "url": "https://www.nandongni.com/"}
{"title": "Waxxh's Blog", "words": "御宅之力，终破次壁", "img": "http://cn.gravatar.com/avatar/54d63390cc597800c3ea2e26a3911e17?s=96&d=mp&r=g", "url": "https://waxxh.me/"}
{"title": "时光博客", "words": "专注于技术热爱与分享", "img": "http://cn.gravatar.com/avatar/8efe463e7dd797fb85b28186008c924a?s=96&d=mp&r=g", "url": "http://sgblog.top"}
......
````

查看了一下，只爬取到一百多条json数据，真实的情况下肯定不止这些了。

后来发现因为成员汇总页博客过多，所以网站是采用懒加载的，而我并不会懒加载。

那么就找教程呗，毕竟面向搜索引擎编程。

## 应对懒加载网站的爬取策略

{% cq %}

若想让页面显示完整须用代码模拟鼠标向下滚动的动作，Selenium就完全可以胜任这个任务。

{% endcq %}

[大神](https://zhuanlan.zhihu.com/p/72887277)给出的方案如下：

> 首先在Scrapy的爬虫主文件中导入Selenium包，具体代码如下：
>
> ````python
> from selenium import webdriver
> class TestSpider(Spider):
>  name = 'test'
>  def __init__(self):
>      self.browser = webdriver.Chrome("chromedriver驱动存放路径")
>      self.browser.set_page_load_timeout(30)
> ````
>
>
> 这仅仅是让Selenium导入到Scarpy中，大多数情况下我们所要抓取的网页都是多页的，而且我们也需要在Selenium执行完向下滚动页面的操作后我们再执行爬取整个页面的代码才能达到预期效果，所以我们需要将Selenium操作页面的代码放入到Scrapy的middlewares.py（中间件）文件中。
>
> 将Selenium滚动页面的代码放入Scrapy的middlewares.py文件中
>
> ````python
> from selenium.common.exceptions import TimeoutException
> class SeleniumMiddleware(object):
>  def process_request(self, request, spider):
>      try:
>          spider.browser.get(request.url)
>          time.sleep(3)
>          spider.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
>          #执行页面下拉操作的代码
>      except TimeoutException as e:
>          print('超时')
>          spider.browser.execute_script('window.stop()')
>      time.sleep(2)
>      return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
>                              encoding="utf-8", request=request)
> ````
>
>
> 这样Scarpy就可以能够抓取到加载完以后的完整数据了。

开始尝试~结果失败了！提示`webdriver`这个包缺失。



## 安装selenium

selenium是一个web自动化测试工具，它可以模拟浏览器中的一些操作，对于一些懒加载的页面，一般是用户滑动到某个位置时才会加载相应的数据，所以可以使用selenium来模拟用户的滑动，从而实现将完整的网页内容加载出来，可以使用下面的命令安装python的selenium库：
`pip install selenium`

## 下载chromedriver驱动

需要和你的chrome浏览器版本保持一致。
[下载地址](https://chromedriver.storage.googleapis.com/index.html)

可以通过`chrome://version/`查看版本，比如这里我可以使用的版本对应为为81.0.4044.xx版本的win版

![mark](https://img.senup.cn/blog/20200430/aLj01kHKPsO1.png?imageslim)

顺便将浏览器chrome.exe加入环境变量Path中。

再把代码添加到pycharm来，开启中间件。



然而报错了。

![mark](https://img.senup.cn/blog/20200430/fdlgXNJ09kfX.png?imageslim)

猜测错误的原因是：大佬给的代码应该只适用普通scrapy爬虫，而加了模板的爬虫还要自定义rules爬取规则因此这个初识化有问题。但是谷歌了一会儿没找到crawlSpider+selenium的帖子，完全没结果！

“ 好恨！ 我怎么这么菜！”

怪自己学爬虫没学精吧，算了算了，这个问题后面有空再解决好了......