import scrapy
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class DtvSpider(scrapy.Spider):
    name = "dtv"
    allowed_domains = ["dtv-ebook.com"]
    start_urls = [
        "https://www.dtv-ebook.com/",
    ]
    rule = Rule(LinkExtractor(allow=r"/[1-3].html"),
             callback="parse_item", follow=True)

    def parse(self, response):
        categories = Selector(response).xpath("/html/body/nav/div/div/nav/section/ul/li[2]/div/ul/li")
        for cate in categories:
            url = cate.xpath("a/@href").extract()[0].split(".html")[0]
            for i in (1, 2, 3):
                url = f"{url}/{i}.html"
            # print(response.urljoin(url))
                yield scrapy.Request(url, callback=self.parse_story)

    def parse_story(self, response):
        item = TutorialItem()
        stories = Selector(response).xpath("/html/body/section[2]/div[2]/div/div/div[1]/div[1]/div/div[2]/ul/li")
        for story in stories:
            item = TutorialItem()
            item["title"] = story.xpath("div/a[1]/@title").extract()[0]
            item["url"] = story.xpath("div/a[1]/@href").extract()[0]
            yield item