from resourceMonitoring import resourceMonitoring
import psutil
import time
import multiprocessing

class cpuMonitoring(resourceMonitoring):

    def __init__(self, resObj):
        super().__init__(resObj)
        self.process = None
        self.output = []

    def getCpu(self):
        while True:
            response = self.resObj.executeCommand(command='top -b -n 10 -d.2 | grep \'Cpu\' |  awk \'NR==3{ print($2)}\';date +\"%d-%m-%y %H:%M:%S\"')
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
        
        

