from datetime import datetime
from bgutils.spider.BaseSpider import BaseSpider

class SpiderHouse(BaseSpider):
    id: str #房产信息ID
    title: str  #房产标题
    house_id: str #房屋ID
    isauction : str #
    city_id : str #所在城市ID
    community_id : str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "house_data" #采集题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充




