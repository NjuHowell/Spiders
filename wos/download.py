import time

from datetime import datetime
from selenium import webdriver
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utils import NjuVpn
from settings import QUEST_URL, QUEST_LENGTH, RECORD_CONTENT, SAVED_OPTION, USER_NAME, PASSWORD

class WosDownloader(object):
    """
    用来自动下载ISI Web Of Knowledge平台的数据
    """

    def __init__(self, quest_url, quest_length, record_content, save_option, is_vpn=False, user_name=None, password=None):
        self.quest_url = quest_url
        self.quest_length = quest_length
        self.record_content = record_content
        self.save_option = save_option
        self.is_vpn = is_vpn
        if self.is_vpn:
            if not user_name:
                raise ValueError("The vpn's user name is not valid.")
            else:
                self.user_name = user_name
            if not password:
                raise ValueError("The vpn's password is not valid.")
            else:
                self.password = password
            nju_vpn = NjuVpn(self.user_name, self.password)
            self.driver = nju_vpn.driver
        else:
            self.driver = webdriver.Chrome()


    def __download_by_index(self, markFrom, markTo):
        if not (isinstance(markFrom, int) and isinstance(markTo, int)):
            raise ValueError('The markFrom and markTo must be integer')
        if (markFrom - markTo + 1) > 500:
            raise ValueError(
                'The differ between markFrom and markTo should not more than 500')
        if (markFrom - markTo) > 0:
            raise ValueError('The markFrom should less than markTo')
        self.driver.get(self.quest_url)

        try:
            save_button = self.driver.find_element_by_id('exportTypeName')
            save_button.click()
            save_menu = self.driver.find_element_by_name('导出为其他文件格式')
            save_menu.click()

        except:
            pass

        # choose the button "download record using index"
        record_range_radio = self.driver.find_element_by_id(
            'numberOfRecordsRange')
        record_range_radio.click()

        # input the range of the index, which is markFrom and markTo
        markFrom_input = self.driver.find_element_by_id('markFrom')
        markTo_input = self.driver.find_element_by_id('markTo')
        markFrom_input.clear()
        markTo_input.clear()
        markFrom_input.send_keys(markFrom)
        markTo_input.send_keys(markTo)

        # choose the button "全记录与引用的参考文献"
        record_content_menu = Select(
            self.driver.find_element_by_name('fields_selection'))
        record_content_menu.select_by_visible_text(self.record_content)

        # choose the button "制表符分割 (Win, UTF-8)"
        save_format_menu = Select(self.driver.find_element_by_id('saveOptions'))
        save_format_menu.select_by_visible_text(self.save_option)

        # download the files
        send_button = self.driver.find_element_by_class_name(
            'quickoutput-action')
        send_button.click()



    def download(self):
        session_length = self.quest_length // 500

        print('Begin to download the datasets.')

        if session_length == 0:
            self.__download_by_index(1, self.quest_length)
        else:
            for index in tqdm(range(0, session_length)):
                markFrom = index * 500 + 1
                markTo = (index + 1) * 500
                self.__download_by_index(markFrom, markTo)
                # sleep ten seconds
                time.sleep(5)
            markFrom = session_length * 500 + 1
            markTo = self.quest_length
            self.__download_by_index(markFrom, markTo)

        print('Finish downloading the datasets.')

if __name__ == '__main__':
    wos_downloader = WosDownloader(quest_url=QUEST_URL, quest_length=QUEST_LENGTH, 
                                    record_content=RECORD_CONTENT, save_option=SAVED_OPTION, 
                                    is_vpn=False, user_name=USER_NAME, password=PASSWORD)
    wos_downloader.download()
    time.sleep(30)
    wos_downloader.driver.close()