# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text

from tutorial.items import TutorialItem


class TutorialPipeline(object):

    def __init__(self):
        _engine = create_engine("sqlite:///data.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _dtv_items = Table("categories", _metadata,
                           Column("id", Integer, primary_key=True),
                           Column("dich_azw3", Text),
                           Column("dich_epub", Text),
                           Column("dich_mobi", Text),
                           Column("dich_pdf", Text),
                           Column("cv_azw3", Text),
                           Column("cv_epub", Text),
                           Column("cv_mobi", Text),
                           Column("cv_pdf", Text),
                           Column("name", Text),
                           Column("author", Text),
                           Column("category", Text),
                           _metadata.create_all(_engine))
        self.connection = _connection
        self._dtv_items = _dtv_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise TutorialItem("Missing %s!" % data)
        if is_valid:
            ins_query = self._dtv_items.insert().values(
                dich_azw3=item["dich_azw3"], dich_epub=item["dich_epub"],dich_mobi=item["dich_mobi"], dich_pdf=item["dich_pdf"], cv_azw3=item["cv_azw3"], cv_epub=item["cv_epub"],cv_mobi=item["cv_mobi"], cv_pdf=item["cv_pdf"],name=item["name"], author=item["author"], category=item["category"])
            self.connection.execute(ins_query)
        return item

    # def process_item(self, item, spider):
    #     return item
