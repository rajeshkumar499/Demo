import timeit
import multiprocessing
import RestAuthentication
import Ssh
import cpuMonitoring
import memoryMonitoring
import logging
LOGGER = logging.getLogger()

@pytest.fixture(scope='module')
def constructor(request):
    """
    Constructor function.

    @param request: MANDATORY Object @n
    used to passed request object

    object passed the testbed configuration
    """
    LOGGER.info('Initial configurations')


@pytest.mark.parametrize(
    'nodeIp',
    [
        {
            'IP1': '1.0.0.21',
            'IP2': '1.0.0.22'
        },
    ],
    ids=[
        'node'
    ]
)
def test_demo(testCase,
              nodeIp):

    urls = [(GET, '/url1'), (POST, '/url2'), (GET, '/url3')]

    #SSH handles for SUT 
    resobj1 = Ssh(nodeIp['IP1'], 'admin', 'admin')
    resobj2 = Ssh(nodeIp['IP2'], 'admin', 'admin')

    #start monitoring parallely
    cpuResObj1 = cpuMonitoring(resobj1))
    cpuResObj2 = cpuMonitoring(resobj2))
    memoryResObj1 = memoryMonitoring(resobj1))
    memoryResObj2 = memoryMonitoring(resobj2))
    
    #getting authentication done and storing token 
    authObj = RestAuthentication('1.1.1.1', 'rajesh', 'kumar')
   
    #sending query 
    for url in urls:
        func = authObj.call_http
        response = authObj.call_http(url[0], url[1])
        if response.ok:
            LOGGER.info('query is successfull. Output is {output}. Time taken to run query is {time} '.format(output=response, time=timeit.timeit(func,1) ))
        else : 
            LOGGER.error('Query Failed')

    #stopping monitoring
    cpuOutput1 = cpuResObj1.stop_monitoring()
    cpuOutput2 = cpuResObj2.stop_monitoring()
    memoryOutput1 = memoryResObj1.stop_monitoring()
    memoryOutput2 = memoryResObj2.stop_monitoring()


    #printing Memory and CPU Data
    LOGGER.info('Memory Data for Node 1: {memoryData}'.format(memoryData=memoryOutput1))
    LOGGER.info('CPU DATA for Node 1: {cpudata}'.format(cpudata=cpuOutput1)) 

    #Same for Node 2
    LOGGER.info('Memory Data for Node 2: {memoryData}'.format(memoryData=memoryOutput1))
    LOGGER.info('CPU DATA for Node 2: {cpudata}'.format(cpudata=cpuOutput2)) 
