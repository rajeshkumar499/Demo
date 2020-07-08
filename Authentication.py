"""Authentication Class to take token for requests."""

import time
import requests
from requests.auth import HTTPBasicAuth
import logging 
LOGGER=logging.getLogger()


class RestAuthentication:
    """Authentication Base class."""



    def __init__(self, ipAddress, username, password):
        """
        Initialisation method.

        @param None

        @return: None
        """
        # authToken
        self._token = None
        # time at which token is created
        self._tokenTime = None
        self.tokenTimeout = 60
        self._ipAddress = ipAddress
        self._username = username
        self._password = password
        self._loginUrl = 'https://{ipaddress}/v1/login.json'.format(ipaddress=self._ipAddress)
        self._headers = None
        fetch_token()
        
    def fetch_token():
        authRes = requests.get(
        self._loginUrl,
        auth=HTTPBasicAuth(
             self._userName,
             self._password)
             )
        if authRes.ok:
           self.setAuthHeaders = authRes.headers
           #self.setAuthCookies = authRes.cookies
           self.setTokenTime = time.time()
        else:
            raise Exception(
               'Auth Request for BasicAuthentication is unsuccessful')
           
    @property
    def getAuthHeaders(self):
        """
        Property to get authentication headers.

        @param None

        @return: dictionary
        """
        return self._headers

    @getAuthHeaders.setter
    def setAuthHeaders(self, headers):
        """
        Property to set authentication header.

        @param headers: MANDATORY ditionary @n

        @return: None
        """
        self._headers = headers

    @property
    def getTokenTime(self):
        """
        Property to get tokenTime.

        @param None

        @return: integer
        """
        return self._tokenTime

    @getTokenTime.setter
    def setTokenTime(self, tokenTime):
        """
        Property to set tokenTime.

        @param tokenTime: MANDATORY integer @n

        @return: None
        """
        self._tokenTime = tokenTime
        
        
    def isAuthTokenValid(self):
        """
        Method to do auth validation.

        @param None

        @return: boolean
        """
        currentTime = time.time()
        timeDiff = currentTime - self.getTokenTime
        if timeDiff >= self.tokenTimeout:
            return False
        else:
            return True
            
    def call_http(method, url, param=None, data=None):
        if isAuthTokenValid():
            pass
        else:
            fetch_token()
        try:
            response = requests.request(method, url, data, param, headers=self._headers) 
            if response.status_code == 200:
                return response, response.json()
            else:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            LOGGER.error('Error occured. ErrorCode:{errorcode}, ErrorMsg:{errormsg}'.format(errorcode=response.status_code,errormsg=err))        


