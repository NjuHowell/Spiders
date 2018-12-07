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
    cookies = [
        'cna=6+4pFE/kuSYCATFNh2m6ulSS; tk_trace=1; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=1ea3dc4557d30c34549fab79fc8fea13; t=ebb017686e037100733241ee35927fc9; _tb_token_=e8d135eeb5b75; _m_h5_tk=3cf8512004e7e8c118b296ff380bc689_1544155907721; _m_h5_tk_enc=1883e0a1265c4140bb0504588df389ba; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=V32FPkk%2FgihF%2FS5nr3O5&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTYMh9%2Fd8ZlFA%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByR1Rmq7LTJBiEvE%3D&id2=UUBaCrGbUPe0UQ%3D%3D&nk2=q7TrYa1zlldecA%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; tracknick=%5Cu8F6F%5Cu59B9%5Cu5C0F%5Cu5929%5Cu5929; _l_g_=Ug%3D%3D; ck1=""; unb=2821216646; lgc=%5Cu8F6F%5Cu59B9%5Cu5C0F%5Cu5929%5Cu5929; cookie1=UNRmagDPcnMNl9nfahZcCYTYjLFEjnh%2FoRK7k9rPcxg%3D; login=true; cookie17=UUBaCrGbUPe0UQ%3D%3D; _nk_=%5Cu8F6F%5Cu59B9%5Cu5C0F%5Cu5929%5Cu5929; uss=""; csg=08f94619; skt=3b2cb2ba3e37a3f8; whl=-1%260%260%260; x5sec=7b22726174656d616e616765723b32223a223537616131336532616564386234346161303633336134303733383237663733434f7135702b4146454c575a2f646e3378742f5651686f4d4d6a67794d5449784e6a59304e6a7378227d; isg=BMjIolGfAOJiMWuwxxOG0QBvmTYa2S1J-PZSPIJ5E8M3XWjHKoBLC7pb0XWI7eRT',
        'tk_trace=1; cna=qMWQFHkT60kCATFNjtOIKXU4; hng=""; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=UtASsssme%2BBq&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTYMh9%2BopwVIw%3D%3D&tag=10&lng=zh_CN; uc3=vt3=F8dByR1RmqxyE8ch6C0%3D&id2=Vv8RRodrTQ%2Fm&nk2=D8ryfCiVc3TNz6bc&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=little08king; _l_g_=Ug%3D%3D; ck1=""; unb=518766202; lgc=little08king; cookie1=UtJRYwo3llkGM8FAMB3vY9Ep3x%2BIn9seFkgypJnbx9U%3D; login=true; cookie17=Vv8RRodrTQ%2Fm; cookie2=1df20dbc9bc16eb2cb49e9205aa47d53; _nk_=little08king; t=e9cd95cb12d463d6cab7b90b38740bff; uss=""; csg=9e5ca109; skt=976457c42e786b5b; _tb_token_=e1e5e7e377eed; _m_h5_tk=a74c60ce97f1751f81eadf31292bc6d4_1544159372849; _m_h5_tk_enc=f3603452de1b758af0074b16150e4236; enc=LvM0mq%2FstAtW8gg5uiBfLSmQc%2FKYySiklQPEoc0hCLRWKVihlOQFufsoj3%2BZWrg1HhSU6XNI3WlorAEmivy%2FIg%3D%3D; isg=BIKCdNKRalS_GHaIK61joPKb04gk-4crY4OxS8ybg_WhHyOZtOJjfX9Zy1vGDf4F',
        'cna=B/9KFKsFfhwCATFNjCwbgRYI; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E6%8A%8A%E6%A0%8F%E6%9D%86%E6%8B%8D%E9%81%8D%E5%8D%83%E5%8F%A4%E9%A3%8E%E6%B5%81; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; enc=Nip0m6wsuzFjgAXuo8PIHdBnss%2Fy67eArBW83w%2Fj99VZq6ppAiDsHexQ2uWHf2h7bvR%2F07nmQAo1EYXxB9Q0aQ%3D%3D; t=713ba899cc048ae53f303e6391b7f733; uc3=vt3=F8dByR1WTOV5GoeSp2M%3D&id2=UU6lRD9SoBM0Xw%3D%3D&nk2=05EkNaTOMZAQg5r8tdzS5XHW&lg2=VT5L2FSpMGV7TQ%3D%3D; tracknick=%5Cu628A%5Cu680F%5Cu6746%5Cu62CD%5Cu904D%5Cu5343%5Cu53E4%5Cu98CE%5Cu6D41; lgc=%5Cu628A%5Cu680F%5Cu6746%5Cu62CD%5Cu904D%5Cu5343%5Cu53E4%5Cu98CE%5Cu6D41; _tb_token_=36836b4e85b3a; cookie2=1c7808e4808c9536f78a22a790dc869a; x5sec=7b22726174656d616e616765723b32223a226331366462363335346531333266636363633030326364666565326537303730434f616a702b4146454c5046302f484e37746e5963673d3d227d; OZ_SI_2061=sTime=1544145772&sIndex=31; OZ_1U_2061=vid=vbe11394852dfc.0&ctime=1544149012&ltime=1544149010; OZ_1Y_2061=erefer=-&eurl=https%3A//detail.tmall.com/item.htm%3Fid%3D574022422774&etime=1544145772&ctime=1544149012&ltime=1544149010&compid=2061; isg=BG5uvwRAvlCsts34q08_nE9Rv8TwxzNeFQ-b4Jg39HEtew_VAP4Lexd9N6cyoyqB',
        'tk_trace=1; cna=WiNMFCLTPGQCATFNjCy7L7ND; dnk=%5Cu5927%5Cu7EA2%5Cu706F%5Cu7B3C%5Cu9AD8%5Cu9AD8%5Cu6302%5Cu7A9D%5Cu7A9D%5Cu5934; uc1=cookie14=UoTYMh9%2BopYRCg%3D%3D&lng=zh_CN&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&existShop=false&cookie21=UIHiLt3xThH8t7YQoFNq&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=vt3=F8dByR1Rmqx4NPtiGc4%3D&id2=UoewAMRENTL5yw%3D%3D&nk2=1z9LFRlABuVWaAYw%2BYDga78f3Dk%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; tracknick=%5Cu5927%5Cu7EA2%5Cu706F%5Cu7B3C%5Cu9AD8%5Cu9AD8%5Cu6302%5Cu7A9D%5Cu7A9D%5Cu5934; lid=%E5%A4%A7%E7%BA%A2%E7%81%AF%E7%AC%BC%E9%AB%98%E9%AB%98%E6%8C%82%E7%AA%9D%E7%AA%9D%E5%A4%B4; _l_g_=Ug%3D%3D; unb=1640614154; lgc=%5Cu5927%5Cu7EA2%5Cu706F%5Cu7B3C%5Cu9AD8%5Cu9AD8%5Cu6302%5Cu7A9D%5Cu7A9D%5Cu5934; cookie1=WvZj8vp7IlpiEJIe9lXmCEuno3LUOk7i7pnoCBOzbt0%3D; login=true; cookie17=UoewAMRENTL5yw%3D%3D; cookie2=1d5f7b7ba827eb6afb39bc403261279a; _nk_=%5Cu5927%5Cu7EA2%5Cu706F%5Cu7B3C%5Cu9AD8%5Cu9AD8%5Cu6302%5Cu7A9D%5Cu7A9D%5Cu5934; t=f524f59667438ccbd81b3eb3ba2a606e; sg=%E5%A4%B44e; csg=a43e138b; _tb_token_=183fa15ebed7; _m_h5_tk=1c94ae7568a050fad347112f668f649e_1544155578900; _m_h5_tk_enc=99551256978be440d555df9d54c24d79; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=BFRUD4Pr9A6_b2BCS3pN3PJkJZIGBXmiYFQmx-41tV952fUjF7wYJjkf3ZFkIbDv'
        ]
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