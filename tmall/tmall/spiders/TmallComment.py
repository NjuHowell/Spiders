import scrapy
import re
import json
import numpy as np

from urllib.parse import urlparse, urlencode

from ..items import TmallItem

class TmallCommentSpider(scrapy.Spider):
    name = 'tmallcomment'
    with open(r'start_urls.txt', 'r') as f_handle:
        start_urls = f_handle.readlines()
        start_urls = [url.strip('\n') for url in start_urls]
    comment_url = 'https://rate.tmall.com/list_detail_rate.htm?'
    item_url = 'https://detail.tmall.com/item.htm?'
    cookies = []
    cookies = [{record.split('=')[0].strip() : record.split('=')[1].strip() for record in cookie.split(';')} for cookie in cookies]
    def start_requests(self):
        for url in self.start_urls:
            params = {str(item.split('=')[0]) : item.split('=')[1] for item in urlparse(url).query.split('&')}
            params['itemId'] = params['id']
            params['sellerId'] = 196993935
            params['currentPage'] = 1
            params.pop('id')
            request_url = self.comment_url + urlencode(params)
            # request_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=574022422774&sellerId=196993935&currentPage=1'
            yield scrapy.Request(request_url, cookies=self.cookies[np.random.randint(0, len(self.cookies))], callback=self.parse)
    
    def parse(self, response):
        comments = json.loads(response.body.decode('utf8')[11:-1])['rateDetail']
        params = {str(item.split('=')[0]) : item.split('=')[1] for item in urlparse(response.url).query.split('&')}
        item_params = dict()
        item_params['id'] = params['itemId']
        if comments.get('rateList'):
            for comment in comments['rateList']:
                t_item = TmallItem()
                t_item['url'] = self.item_url + urlencode(item_params)
                t_item['rateDate'] = comment.get('rateDate')
                t_item['rateContent'] = json.dumps(comment.get('rateContent'))
                t_item['auctionSku'] = json.dumps(comment.get('auctionSku'))
                t_item['rateCount'] = json.dumps(comments.get('rateCount'))
                t_item['tags'] = json.dumps(comments.get('tags'))
                yield t_item
        next_url = None
        if (comments.get('paginator') and comments.get('paginator').get('page') and comments.get('paginator').get('lastPage')) and (comments.get('paginator').get('page') < comments.get('paginator').get('lastPage')) and (comments.get('paginator').get('page') < 8):
            params['currentPage'] = comments['paginator']['page'] + 1
            next_url = self.comment_url + urlencode(params)
        if next_url:
            yield scrapy.Request(next_url, cookies=self.cookies[np.random.randint(0, len(self.cookies))], callback=self.parse)