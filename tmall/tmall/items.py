# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    rateDate = scrapy.Field()
    rateContent = scrapy.Field()
    auctionSku = scrapy.Field()
    rateCount = scrapy.Field()
    tags = scrapy.Field()
    pass
