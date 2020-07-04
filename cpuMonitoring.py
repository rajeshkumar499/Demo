from resourceMonitoring import resourceMonitoring

class cpuMonitoring(resourceMonitoring):

    def __init__(self, resObj):
        super().__init__(resObj)
        self.output = dict()

    def monitoring(self):
        while True:
            response = self.resObj.executeCommand(command='top -b -n 10 -d.2 | grep \'Cpu\' |  awk \'NR==3{ print($2)}\';date +\"%d-%m-%y %H:%M:%S\"')
            output1=response.split('\n')
            self.output[output1[1]] = output1[0]
            time.sleep(2)

