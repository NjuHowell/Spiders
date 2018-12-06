import scrapy
import re
import json

from urllib.parse import urlparse, urlencode

from ..items import TmallItem

class TmallCommentSpider(scrapy.Spider):
    name = 'tmallcomment'
    start_urls = ['https://detail.tmall.com/item.htm?id=574022422774']
    comment_url = 'https://rate.tmall.com/list_detail_rate.htm?'
    item_url = 'https://detail.tmall.com/item.htm?'
    cookies = 'cna=B/9KFKsFfhwCATFNjCwbgRYI; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E6%8A%8A%E6%A0%8F%E6%9D%86%E6%8B%8D%E9%81%8D%E5%8D%83%E5%8F%A4%E9%A3%8E%E6%B5%81; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; enc=Nip0m6wsuzFjgAXuo8PIHdBnss%2Fy67eArBW83w%2Fj99VZq6ppAiDsHexQ2uWHf2h7bvR%2F07nmQAo1EYXxB9Q0aQ%3D%3D; t=713ba899cc048ae53f303e6391b7f733; uc3=vt3=F8dByR1WTOV5GoeSp2M%3D&id2=UU6lRD9SoBM0Xw%3D%3D&nk2=05EkNaTOMZAQg5r8tdzS5XHW&lg2=VT5L2FSpMGV7TQ%3D%3D; tracknick=%5Cu628A%5Cu680F%5Cu6746%5Cu62CD%5Cu904D%5Cu5343%5Cu53E4%5Cu98CE%5Cu6D41; lgc=%5Cu628A%5Cu680F%5Cu6746%5Cu62CD%5Cu904D%5Cu5343%5Cu53E4%5Cu98CE%5Cu6D41; _tb_token_=e704ee08ef543; cookie2=1c03334c83582ca263c344f72778a21b; OZ_SI_2061=sTime=1544076652&sIndex=4; OZ_1U_2061=vid=vbe11394852dfc.0&ctime=1544076664&ltime=1544076661; OZ_1Y_2061=erefer=-&eurl=https%3A//detail.tmall.com/item.htm%3Fid%3D574022422774&etime=1544076652&ctime=1544076664&ltime=1544076661&compid=2061; isg=BAMDfnOnW2J8RRBbRvh679qeksdt0JaNgDCmQzXgHGLZ9CIWvUmDCIAiasQf1O-y'
    cookies = {
        record.split('=')[0].strip() : record.split('=')[1].strip() for record in cookies.split(';')
    }
    def start_requests(self):
        for url in self.start_urls:
            params = {str(item.split('=')[0]) : item.split('=')[1] for item in urlparse(url).query.split('&')}
            params['itemId'] = params['id']
            params['sellerId'] = 196993935
            params['currentPage'] = 1
            params.pop('id')
            request_url = self.comment_url + urlencode(params)
            yield scrapy.Request(request_url, cookies=self.cookies, callback=self.parse)
    
    def parse(self, response):
        t_item = TmallItem()
        # split the comments
        comments = json.loads(response.body.decode('utf8')[11:-1])['rateDetail']
        t_item['comments'] = comments
        params = {str(item.split('=')[0]) : item.split('=')[1] for item in urlparse(response.url).query.split('&')}
        item_params = dict()
        item_params['id'] = params['itemId']
        t_item['url'] = self.item_url + urlencode(item_params)
        yield t_item

        next_url = None
        if (comments.get('paginator') and comments.get('paginator').get('page') and comments.get('paginator').get('lastPage')) and (comments.get('paginator').get('page') < comments.get('paginator').get('lastPage')):
            params['currentPage'] = comments['paginator']['page'] + 1
            next_url = self.comment_url + urlencode(params)
        if next_url:
            yield scrapy.Request(next_url, cookies=self.cookies, callback=self.parse)