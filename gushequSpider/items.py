# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GushequspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    entry_date_published = scrapy.Field()
    rich_media_content = scrapy.Field()
    discuss_container = scrapy.Field()
    




