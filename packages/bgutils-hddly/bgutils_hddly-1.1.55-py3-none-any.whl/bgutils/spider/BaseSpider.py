import abc
from dataclasses import dataclass

@dataclass
class BaseSpider(metaclass=abc.ABCMeta):
    # @abc.abstractmethod
    # def my_abstract_method(self):
    #     pass

    topic: str
    rawurl: str
    rawdata: str

    username: str
    collector: str
    coll_time: str

    def __init__(self, username, collector, topic, rawurl, rawdata):
        return
        # self.username = username,
        # self.collector = collector,
        # self.topic = topic,
        # self.rawurl = rawurl,
        # self.rawdata = rawdata,


    # def to_dict(self):
    #     return self.__dict__

