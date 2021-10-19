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
                             Column("url", Text),
                             Column("title", Text))
        _metadata.create_all(_engine)
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
                url=item["url"], title=item["title"])
            self.connection.execute(ins_query)
        return item

    # def process_item(self, item, spider):
    #     return item
