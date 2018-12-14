import scrapy
import json
import re

from ..items import JdEbookBestsellerItem
from urllib.parse import urlparse, urlencode

class jd_ebook_bestseller(scrapy.Spider):
    name = 'jd_ebook'
    price_seed = 'https://p.3.cn/prices/mgets?'
    comment_seed = 'https://club.jd.com/comment/productCommentSummaries.action?'
    start_urls = [
        'http://e.jd.com/rank/5272-0-15-1.html',
        'http://e.jd.com/rank/5272-0-15-2.html',
        'http://e.jd.com/rank/5272-0-15-3.html',
        'http://e.jd.com/rank/5272-0-15-4.html',
        'http://e.jd.com/rank/5272-0-15-5.html'
    ]

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath("//div[@class='mcc']/div[@class='item']/dl/dt[@class='p-name']/a/@href").extract():
            item_url = 'http:' + url
            yield scrapy.Request(url=item_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item =JdEbookBestsellerItem()
        name = json.dumps(response.xpath("//div[@class='sku-name']/text()").extract_first())
        author = json.dumps(response.xpath("//div[@class='author']/a/text()").extract_first())
        bookinfo = dict()
        for info_item in response.xpath("//div[@class='bookInfo']/div[@class='li']//div[@class='infoItem']"):
            key = info_item.xpath('div[1]/text()').extract_first()
            value = info_item.xpath('div[2]/text()').extract_first()
            if isinstance(key, str):
                bookinfo[key] = json.dumps(value)
        category = json.dumps(response.xpath("//div[@class='category li']/div[@class='dd']/a/text()").extract_first())
        # 获取商品id
        item_id = re.findall(
            pattern=r'[0-9]+', 
            string=urlparse(response.url).path
        )[0]
        item['url'] = response.url
        item['item_id'] = item_id
        item['name'] = name
        item['author'] = author
        item['bookinfo'] = bookinfo
        item['category'] = category
        # 获取商品价格详情
        price_params = {
            'skuids' : 'J_' + item_id
        }
        price_request = scrapy.Request(self.price_seed + urlencode(price_params), callback=self.parse_price)
        price_request.meta['item'] = item
        price_request.meta['skuids'] = price_params['skuids']
        yield price_request
    
    def parse_price(self, response):
        item = response.meta['item']
        skuids = response.meta['skuids']
        price_detail = json.loads(response.body.decode('utf8'))
        original_price = None
        price = None
        paper_price = None
        for item_price in price_detail:
            if item_price.get('id') == skuids:
                original_price = item_price.get('op')
                price = item_price.get('p')
                paper_price = item_price.get('m')
                break
            else:
                pass
        item['original_price'] = original_price
        item['price'] = price
        item['paper_price'] = paper_price
        comment_params = {
            'referenceIds' : item['item_id']
        }
        comment_request = scrapy.Request(self.comment_seed + urlencode(comment_params), callback=self.parse_comment)
        comment_request.meta['item'] = item
        yield comment_request

    def parse_comment(self, response):
        item = response.meta['item']
        CommentCount, AverageScore, GoodCount, PoorCount, VideoCount = [None for i in range(5)]
        comment_detail = json.loads(response.body.decode('gbk'), strict=False).get('CommentsCount')
        if comment_detail:
            for item_comment in comment_detail:
                if str(item_comment.get('ProductId')) == item['item_id']:
                    CommentCount = item_comment.get('CommentCount')
                    AverageScore = item_comment.get('AverageScore')
                    GoodCount = item_comment.get('GoodCount')
                    PoorCount = item_comment.get('PoorCount')
                    VideoCount = item_comment.get('VideoCount')
                    break
                else:
                    pass
        item['CommentCount'] = CommentCount
        item['AverageScore'] = AverageScore
        item['GoodCount'] = GoodCount
        item['PoorCount'] = PoorCount
        item['VideoCount'] = VideoCount
        yield item 

# # 京东获取评论详情的url
# comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=30383844'
# # 京东商品价格url
# price_url = 'https://p.3.cn/prices/mgets?skuids=J_30383844'