from datetime import datetime

class SpiderBook():
    title: str
    author: str
    link: str
    desc: str
    price: str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username
        self.collector= collector
        self.topic = "books_data"
        self.rawurl= rawurl
        self.rawdata = rawdata
        self.coll_time = datetime.now()
