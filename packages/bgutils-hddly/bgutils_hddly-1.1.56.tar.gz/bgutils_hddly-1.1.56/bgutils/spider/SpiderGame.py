from datetime import datetime

class SpiderGame():
    id: str
    title: str
    playlink: str
    introduce: str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username
        self.collector= collector
        self.topic = "games_data"
        self.rawurl= rawurl
        self.rawdata = rawdata
        self.coll_time = datetime.now()
