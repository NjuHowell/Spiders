# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdEbookBestsellerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rank = scrapy.Field()
    url = scrapy.Field()
    item_id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    bookinfo = scrapy.Field()
    category = scrapy.Field()
    original_price = scrapy.Field()
    price = scrapy.Field()
    paper_price = scrapy.Field()
    CommentCount = scrapy.Field()
    AverageScore = scrapy.Field()
    GoodCount = scrapy.Field()
    PoorCount = scrapy.Field()
    VideoCount = scrapy.Field()
    pass
