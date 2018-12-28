import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode, unquote, quote

class WOS(object):
    def __init__(self, query_url, query_length):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
            }
        self.query_url = query_url
        self.query_length = query_length
        self.tagged_list_url = 'http://apps.webofknowledge.com/MarkRecords.do?'
        self.download_page_url_post = 'http://apps.webofknowledge.com/OutboundService.do?'
        self.download_page_url_get = 'http://ets.webofknowledge.com/ETS/ets.do?'
        self.erase_tagged_list_url = 'http://apps.webofknowledge.com/DeleteMarked.do?'
    
    def parse_query_items(self):
        # query_url = self.query_url
        # 爬取self.query_url页面内容，获取检索总条数
        # 考虑到wos页面的反爬机制，检索条数作为关键词已经被屏蔽，后期使用其他方法进行处理
        return
    
    def add_to_tagged_result_list(self, ids):
        '''
        将检索结果界面中的结果根据id添加到标记结果列表
        注意：标记结果列表最多不超过500条，
        @args
            ids: string, 形如'1;2;3;...'
        @returns
        '''
        # 表单数据
        data = {
            'selectedIds' : ids,
            'colName' : 'WOS',
            'viewType' : 'summary'
        }
        # 传入参数
        query_params = urlparse(self.query_url).query
        query_params = {
            record.split('=')[0] : record.split('=')[1] for record in query_params.split('&')
        }
        params = {
            'product' : 'WOS',
            'mark_id' : 'UDB',
            'SID' : query_params['SID'],
            'qid' : '1',
            'search_mode' : 'GeneralSearch'
        }
        post_url = self.tagged_list_url + urlencode(params)
        requests.post(url=post_url, data=data, headers=self.headers)
        return len(ids.split(';'))
    
    def download_from_tagged_result_list(self, length, file_path):
        '''
        将标记结果列表中标记的所有数据下载下来，进行如下两个步骤
        1) 向http://apps.webofknowledge.com/OutboundService.do? post所要下载的数据清单
        2) 向http://ets.webofknowledge.com/ETS/ets.do?请求数据
        3) 将所请求到的数据下载下来
        @args
            length: 标记结果列表结果数量
            file_path: 存放结果的文件路径
        @returns
        '''
        if length >500 or length < 1:
            raise ValueError("The length must in [1, 500]")
        # 进行post操作
        query_params = urlparse(self.query_url).query
        query_params = {
            record.split('=')[0]: record.split('=')[1] for record in query_params.split('&')
        }

        post_params = {
            'action' : 'go',
            'totalMarked' : length
        }
        post_data = {
            'displayCitedRefs' : 'true',
            'displayTimesCited' : 'true',
            'displayUsageInfo' : 'true',
            'viewType' : 'summary',
            'product' : 'WOS',
            'mark_id' : 'WOS',
            'colName' : 'WOS',
            'search_mode' : 'MarkedList',
            'locale' : 'zh_CN',
            'view_name': 'WOS-MarkedList-summary',
            'sortBy': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A',
            'mode' : 'OpenOutputService',
            'qid' : '3025',
            'SID' : query_params['SID'],
            'format' : 'saveToFile',
            'filters': 'AUTHORS+TITLE+SOURCE+CONFERENCE_INFO+CITREF+DOCTYPE+CITTIMES+KEYWORDS+ISSN+CITREFC+SABBR+JCR_CATEGORY+ACCESSION_NUM+AUTHORSIDENTIFIERS+PMID',
            'mark_from' : '1',
            'mark_to' : str(length),
            'queryNatural': '<b>来自于+标记结果列表:</b>+',
            'count_new_items_marked' : '0',
            'use_two_ets' : 'false',
            'IncitesEntitled' : 'no',
            'save_options' : 'tabWinUTF8',
            'value(ml_output_options)' : 'show',
            'totalMarked' : str(length),
            'value(record_select_type)' : 'allrecords',
            'selectedQOFormat' : 'other',
            'saveToMenu' : 'other',
            'fields' : [
                'AUTHORS', 'TITLE', 'SOURCE', 'CONFERENCE_INFO', 'CITREF', 'DOCTYPE', 'CITTIMES', 'KEYWORDS', 
                'ISSN', 'CITREFC', 'SABBR', 'JCR_CATEGORY', 'ACCESSION_NUM', 'AUTHORSIDENTIFIERS', 'PMID'
            ],
            'rurl' : [
                self.query_url + 'qid=' + '1',
                'http://apps.webofknowledge.com/ViewMarkedList.do?' + urlencode({
                    'action' : 'Search',
                    'product' : 'WOS',
                    'SID' : query_params['SID'],
                    'mark_id' : 'UDB',
                    'search_mode' : 'MarkedList',
                    'colName' : 'WOS',
                    'entry_prod' : 'WOS'
                }),
                self.query_url + 'qid=' + '1',
            ]
        }
        post_url = self.download_page_url_post + urlencode(post_params)
        requests.post(url=post_url, data=post_data, headers=self.headers)

        # 进行get操作，从wos服务器下载数据
        get_params = {
            'mark_from' : post_data['mark_from'],
            'product' : 'UA',
            'colName' : 'WOS',
            'displayUsageInfo' : post_data['displayUsageInfo'],
            'parentQid' : post_data['qid'],
            # 'rurl' : post_data['rurl'][0],
            'rurl': post_data['rurl'][0],
            'mark_to' : post_data['mark_to'],
            'filters': 'AUTHORS TITLE SOURCE CONFERENCE_INFO CITREF DOCTYPE CITTIMES KEYWORDS ISSN CITREFC SABBR JCR_CATEGORY ACCESSION_NUM AUTHORSIDENTIFIERS PMID',
            'qid' : '3026',
            'SID' : post_data['SID'],
            'totalMarked' : post_data['totalMarked'],
            'action' : post_data['format'],
            'sortBy' : post_data['sortBy'],
            'displayTimesCited' : post_data['displayTimesCited'],
            'displayCitedRefs' : post_data['displayCitedRefs'],
            'fileOpt' : post_data['save_options'],
            'UserIDForSaveToRid' : 'null'
        }
        get_url = self.download_page_url_get + urlencode(get_params)
        download_results = requests.get(url=get_url, headers=self.headers)
        with open(file_path, 'w', encoding='utf8') as f_handle:
            f_handle.write(download_results.text)
        
    def erase_tagged_result_list(self):
        '''
        清除标记结果列表
        '''
        query_params = urlparse(self.query_url).query
        query_params = {
            record.split('=')[0]: record.split('=')[1] for record in query_params.split('&')
        }
        erase_params = {
            'search_mode' : 'MarkedList',
            'product' : 'WOS',
            'mark_id' : 'UDB',
            'SID' : query_params['SID'],
            'colName' : 'WOS',
            'qid' : '1'
        }
        erase_url = self.erase_tagged_list_url + urlencode(erase_params)
        requests.get(erase_url, headers=self.headers)

if __name__ == '__main__':
    wos_url = 'http://apps.webofknowledge.com/Search.do?product=WOS&SID=8BN2M8uK5JlqmD9BvIb&search_mode=GeneralSearch&prID=350fd29f-3eae-44b8-926b-01cc99ef6f93'
    length = 3342
    wos = WOS(wos_url, length)
    # numbers = length // 500
    # if numbers <= 1:
    #     wos.add_to_tagged_result_list(';'.join([str(i) for i in range(1, length + 1)]))
    #     wos.download_from_tagged_result_list(length, r'download.txt')
    # else:
    #     for index in range(0, numbers):
    #         start = index * 500 + 1
    #         end = (index + 1) * 500 + 1
    #         wos.add_to_tagged_result_list(';'.join([str(i) for i in range(start, end)]))
    #         wos.download_from_tagged_result_list(500, file_path=str(index) + '.txt')
    #         wos.erase_tagged_result_list()
    # wos.erase_tagged_result_list()
    wos.add_to_tagged_result_list(';'.join([str(i) for i in range(501, 751)]))
    wos.download_from_tagged_result_list(250, r'test.txt')
