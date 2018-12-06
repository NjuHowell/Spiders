# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class TmallPipeline(object):
    def process_item(self, item, spider):
        # item['comments'] = json.dumps([record['rateContent'] for record in item['comments']['rateList']])
        comments = []
        if not isinstance(item['comments'], dict):
            item['comments'] = json.dumps(comments)
            return item
        if item['comments'].get('rateList') == None:
            item['comments'] = json.dumps(comments)
            return item
        for record in item['comments']['rateList']:
            if record.get('rateContent') != None:
                comments.append(record['rateContent'])
        item['comments'] = json.dumps(comments)
        return item
