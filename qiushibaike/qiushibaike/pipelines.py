# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from qiushibaike import settings

class QiushibaikePipeline:

    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        self.db = self.connection[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLL]

    def process_item(self, item, spider):
        if not self.connection or not item:
            return
        postItem = dict(item)
        self.collection.insert_one(postItem)

    def __del__(self):
        if self.connection:
            self.connection.close()
