# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class GushequspiderPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(r"mongodb://127.0.0.1:27017")
        db = client["Gushequ"]
        self.post = db["大牛猫心血"]





    def process_item(self, item, spider):
        postItem = dict(item)
        self.post.insert(postItem)
        return item
