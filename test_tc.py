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
    p = multiprocessing.Process(target=cpuMonitoring(resobj1))
    q = multiprocessing.Process(target=cpuMonitoring(resobj2))
    r = multiprocessing.Process(target=memoryMonitoring(resobj1))
    s = multiprocessing.Process(target=memoryMonitoring(resobj2))
    p.start()
    q.start()
    r.start()
    s.start()
   
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

    # stoping all monitoring
    p.terminate()
    q.terminate()
    r.terminate()
    s.terminate()

    p.join()
    q.join()
    r.join()
    s.join()

    #printing Memory and CPU Data
    LOGGER.info('Memory Data for Node 1: {memoryData}'.format(memoryData=memoryMonitoring(resobj1).output))
    LOGGER.info('CPU DATA for Node 1: {cpudata}'.format(cpudata=cpuMonitoring(resobj1).output)) 

    #Same for Node 2
