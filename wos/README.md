# ISI Web of knowledge 题录自动下载工具
## 1. dependency
* selenium

## 2. selenium模拟浏览器下载
### 2.1 download chromedriver
```simulate_browser.py```采用```selenium + chromedriver```模拟浏览器行为，实现WOS题录数据的自动下载，因而首先需要下载```chromedriver```，```chromedriver```下载地址如下：

Windows端Chrome driver下载: [Windows](http://npm.taobao.org/mirrors/chromedriver/70.0.3538.97/)

Mac端Chrome driver: [Mac](http://npm.taobao.org/mirrors/chromedriver/70.0.3538.97/)

下载完成后，将chromedriver解压放到Python的根目录下。

### 2.2 parameters
该项目中，有两处需要进行修改。
* ```settings.QUEST_URL```: 将此处修改为检索结果的网页链接
* ```settings.QUEST_LENGTH```: 将此处修改为检索结果的条数

### 2.3 run
进入到```simulate_browser.py```路径下，直接运行```python simulate_browser.py```

## 3. 通过抓包分析，自动下载题录信息
Still working on, please wait.