from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider


class SpiderNews(BaseSpider):
    newsTitle: str
    newsUrl: str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username
        self.collector= collector
        self.topic = "news_data"
        self.rawurl= rawurl
        self.rawdata = rawdata
        self.coll_time = datetime.now()