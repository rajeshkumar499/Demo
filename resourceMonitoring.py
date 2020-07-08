from abc import ABCMeta, abstractmethod

class resourceMonitoring(Object):
    def __init__(self, resObj):
        self.resObj = resObj

    @abstractmethod
    def start_monitoring(self):		
        pass

    @abstractmethod
    def stop_monitoring(self):
        pass

