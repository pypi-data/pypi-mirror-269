from datetime import datetime

class SpiderVideo():
    aid: str
    bvid: str
    typename: str
    title: str
    play: str
    author: str
    pic: str
    duration: str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username
        self.collector= collector
        self.topic = "videos_data"
        self.rawurl= rawurl
        self.rawdata = rawdata
        self.coll_time = datetime.now()
