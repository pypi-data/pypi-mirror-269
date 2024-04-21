from datetime import datetime
from bgutils.spider.BaseSpider import BaseSpider

class SpiderHouse(BaseSpider):
    id: str
    title: str
    house_id: str
    isauction : str
    city_id : str
    community_id : str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username
        self.collector= collector
        self.topic = "house_data"
        self.rawurl= rawurl
        self.rawdata = rawdata
        self.coll_time = datetime.now()



