from resourceMonitoring import resourceMonitoring

class memoryMonitoring(resourceMonitoring):

    def __init__(self, resObj):
        super().__init__(resObj)
        self.output = dict()

    def monitoring(self):
        while True:
            response = self.resObj.executeCommand(command='free -m | awk \'NR==2{printf \"%.2f\n\", $3*100/$2 }\';date +\"%d-%m-%y %H:%M:%S\"')
            output1=response.split('\n')
            self.output[output1[1]] = output1[0]
            time.sleep(2)



from resourceMonitoring import resourceMonitoring
import psutil
import time
import multiprocessing

class memoryMonitoring(resourceMonitoring):

    def __init__(self, resObj):
        super().__init__(resObj)
        self.process = None
        self.output = []

    def getCpu(self):
        while True:
            response = self.resObj.executeCommand(command='free -m | awk \'NR==2{printf \"%.2f\n\", $3*100/$2 }\';date +\"%d-%m-%y %H:%M:%S\"')
            response = response.split('\n')
            self.output[response[1]] = response[0]
            time.sleep(2)
            
    def start_monitoring(self):
        self.process = multiprocessing.Process(target=self.getCpu)
        self.process.start()
            
    def stop_monitoring(self):
        self.process.terminate()
        self.process.join()
        return(self.output)