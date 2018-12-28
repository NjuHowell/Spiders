import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from settings import QUEST_URL, QUEST_LENGTH


def download_by_index(driver, QUEST_URL, markFrom, markTo):
    if  not (isinstance(markFrom, int) and isinstance(markTo, int)):
        raise ValueError('The markFrom and markTo must be integer')
    if (markFrom - markTo + 1) > 500:
        raise ValueError('The differ between markFrom and markTo should not more than 500')
    if (markFrom - markTo) >= 0:
        raise ValueError('The markFrom should less than markTo')
    driver.get(QUEST_URL)

    save_button = driver.find_element_by_class_name('saveToButton')
    save_menu = Select(driver.find_element_by_id('saveToMenu'))
    save_menu.select_by_visible_text('保存为其他文件格式')

    # choose the button "download record using index"
    record_range_radio = driver.find_element_by_id('numberOfRecordsRange')
    record_range_radio.click()

    # input the range of the index, which is markFrom and markTo
    markFrom_input = driver.find_element_by_id('markFrom')
    markTo_input = driver.find_element_by_id('markTo')
    markFrom_input.clear()
    markTo_input.clear()
    markFrom_input.send_keys(markFrom)
    markTo_input.send_keys(markTo)

    # choose the button "全记录与引用的参考文献"
    record_content_menu = Select(driver.find_element_by_name('fields_selection'))
    record_content_menu.select_by_visible_text('全记录与引用的参考文献')

    # choose the button "制表符分割 (Win, UTF8)"
    save_format_menu = Select(driver.find_element_by_id('saveOptions'))
    save_format_menu.select_by_value('tabWinUTF8')

    # download the files
    send_button = driver.find_element_by_class_name('quickoutput-action')
    send_button.click()

    # # close the session
    # close_session_button = driver.find_element_by_class_name('quickoutput-cancel-action')
    # close_session_button.click()
    return


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = QUEST_URL
    length = QUEST_LENGTH
    session_length = length // 500

    if session_length == 0:
        download_by_index(driver, url, 1, length)
    else:
        for index in range(0, session_length):
            markFrom = index * 500 + 1
            markTo = (index + 1) * 500
            download_by_index(driver, url, markFrom, markTo)
            # sleep ten seconds
            time.sleep(10)
        markFrom = session_length * 500 + 1
        markTo = length
        download_by_index(driver, url, markFrom, markTo)
    # close the chrome driver
    # driver.close()