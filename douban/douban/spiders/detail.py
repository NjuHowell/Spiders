import scrapy

from scrapy import Request
from ..items import MovieDetailItem

class MovieDetailSpider(scrapy.Spider):
    name = 'moviedetail'
    
    with open(r'start_urls.txt', 'r') as f_handle:
        start_urls = [line.strip('\n') for line in f_handle.readlines()]

    def start_requests(self):
        for url in self.start_urls:
            headers = {
                'Referer' : url,
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
            }
            yield Request(url=url, headers=headers, callback=self.parse)
    
    def parse(self, response):
        md_item = MovieDetailItem()
        url = response.url
        name = response.xpath("//div[@id='content']/h1/span[1]/text()").extract_first()
        movie_info = response.xpath("//div[@id='info']")
        md_item['url'] = url
        md_item['name'] = name
        yield md_item



