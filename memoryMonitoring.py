
from resourceMonitoring import resourceMonitoring
import psutil
import time
import multiprocessing

class memoryMonitoring(resourceMonitoring):

    def __init__(self, resObj):
        super().__init__(resObj)
        self.process = None
        self.output = []

    def getMemory(self):
        while True:
            response = self.resObj.executeCommand(command='free -m | awk \'NR==2{printf \"%.2f\n\", $3*100/$2 }\';date +\"%d-%m-%y %H:%M:%S\"')
            response = response.split('\n')
            self.output[response[1]] = response[0]
            time.sleep(2)
            
    def start_monitoring(self):
        self.process = multiprocessing.Process(target=self.getMemory)
        self.process.start()
            
    def stop_monitoring(self):
        self.process.terminate()
        self.process.join()
        return(self.output)