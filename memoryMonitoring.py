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

