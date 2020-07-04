from abc import ABCMeta, abstractmethod

class resourceMonitoring(Object):
    def __init__(self, resObj):
        self.resObj = resObj

    @abstractmethod
    def monitoring(self):		
        pass


