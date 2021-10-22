import scrapy
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json


result = dict()
class DtvSpider(scrapy.Spider):
    name = "dtv"
    allowed_domains = ["dtv-ebook.com"]
    start_urls = [
        "https://www.dtv-ebook.com/",
    ]
    rule = Rule(LinkExtractor(allow=r"/[1-5].html"),
             callback="parse", follow=True)

    def parse(self, response):
        categories = Selector(response).xpath("/html/body/nav/div/div/nav/section/ul/li[2]/div/ul/li")
        for cate in categories:
            url = cate.xpath("a/@href").extract()[0].split(".html")[0]
            for i in (1, 2, 3, 4, 5):
                tmp = f"{url}/{i}.html"
            # print(response.urljoin(url))
                yield scrapy.Request(tmp, callback=self.parse_story)

    def parse_story(self, response):
        item = TutorialItem()
        stories = Selector(response).xpath("/html/body/section[2]/div[2]/div/div/div[1]/div[1]/div/div[2]/ul/li")
        for story in stories:
            # item = TutorialItem()
            # item["title"] = story.xpath("div/a[1]/@title").extract()[0]
            url = story.xpath("div/a[1]/@href").extract()[0]
            # print("URL: ", url)
            yield scrapy.Request(url=url+"#download", callback=self.parse_data)

    def parse_data(self, response):
        item = TutorialItem()

        informations = Selector(response).xpath('//*[@class="tblChiTietDiDong"]')
        name = informations.xpath("tr[1]/td/h2/text()").extract()[0].strip()
        result[name] = []

        result[name].append(informations.xpath("tr[2]/td[2]/a/text()").extract()[0].strip())

        result[name].append(informations.xpath("tr[4]/td[2]/a/text()").extract()[0].strip())


        rows = Selector(response).xpath('//*[@id="download"]/table/tr')
        if rows is None:
            rows = Selector(response).xpath('//*[@id="download"]/table/tr')
            if rows is None:
                rows = Selector(response).xpath('//*[@id="download"]/table/tr')
        for row in rows:
            atags = row.xpath("td/a")
            for atag in atags[1:]:
                result[name].append({atag.xpath("@title").extract()[0].strip() : atag.xpath("@href").extract()[0].strip()})

        with open("data.json", "w") as f:
            json.dump(result, f)



        # yield item

