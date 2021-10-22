# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dich_azw3 = scrapy.Field()
    dich_epub = scrapy.Field()
    dich_mobi = scrapy.Field()
    dich_pdf = scrapy.Field()
    cv_azw3 = scrapy.Field()
    cv_epub = scrapy.Field()
    cv_mobi = scrapy.Field()
    cv_pdf = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
#
#
#
# Column("dich_azw3", Text),
#                            Column("dich_epub", Text),
#                            Column("dich_mobi", Text),
#                            Column("dich_pdf", Text),
#                            Column("cv_azw3", Text),
#                            Column("cv_epub", Text),
#                            Column("cv_mobi", Text),
#                            Column("cv_pdf", Text),
#                            Column("name", Text),
#                            Column("author", Text),
#                            Column("category", Text),
