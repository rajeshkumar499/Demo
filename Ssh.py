"""
Provides APIs to execute commands over ssh.

"""

import os
import re
import time
import uuid
import errno
import socket
import paramiko
import warnings
import cryptography
import logging 
LOGGER=logging.getLogger() 



class Ssh:
    """Ssh wrapper class over paramiko."""

    def __init__(self, host, user, password, privateKeyFile=None, port=22):
        """
        Initialization method (constructor).

        @param host: MANDATORY string @n
            IP address or DNS of the device to connect
        @param port (22): OPTIONAL integer @n
            SSH port to connect
        @param user: MANDATORY string @n
            user to establish ssh connection with
        @param password: MANDATORY string @n
            password for the specified username
        @param privateKeyFile (None): OPTIONAL string @n
            file containing the private key to be used for authentication
   

        @return: None

        Note:
        1. Password can be specified as an empty string, when connecting to
           a host with passwordless ssh enabled.

        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.privateKeyFile = privateKeyFile
        self.connection = None
       

    def connect(self, connectionTimeout=30):
        """
        Establish SSH connection.

        @param connectionTimeout (30): OPTIONAL integer @n
            Connection timeout in seconds

        Guarantees:
            - Throws an exception if the connection couldn't be established.



        @return: None
        """
        sshConn = paramiko.SSHClient()
        try:
            sshConn.load_system_host_keys()
        except Exception:
            LOGGER.error("Exception occured while loading system keys for connecting " +
                         "to device. So now going ahead with trying to add the hostname " +
                         "and new host key to the local HostKey Object and saving it.")
        finally:
            sshConn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshConn.connect(hostname=self.host,
                        port=self.port,
                        username=self.user,
                        password=self.password,
                        key_filename=self.privateKeyFile,
                        timeout=connectionTimeout)
        self.connection = sshConn

    def _isConnectionActive(self):
        """
        Check if the connection is active.

        @return: True, if the connection is active
                 False, otherwise
        """
        if (self.connection is None or
            not (self.connection.get_transport() and
                 self.connection.get_transport().is_active())):
            return False
        return True

    def executeCommand(self,
                       command,
                       executionTimeout=30,
                       connectionTimeout=30,
                       refreshConnection=False,
                       sudo=False):
        """
        Execute command over ssh connection.

        Guarantees:
            - An attempt to establish a connection will be made,
              if the connection doesn't exist already. An exception will be
              thrown if the attempt does not succeed.
            - A response will be returned with exitCode equals to
              'errno.ETIME' (Timer expired) and stdOut and stdErr each equal to
              None.
            - An exception will be thrown if command could not be executed for
              any other reason.

        @param command: MANDATORY string @n
            Command to be executed
        @param executionTimeout (30): OPTIONAL integer @n
            Command execution timeout in seconds
        @param connectionTimeout (30): OPTIONAL integer @n
            Connection timeout in seconds
        @param refreshConnection (False): OPTIONAL boolean @n
            Flag to force establish a new connection
        @param sudo (False): OPTIONAL boolean @n
            Run specified command with sudo privileges
            - prefix command with 'sudo ', if True
            - run command as it is, otherwise

        @return: A dictionary containing stdout, stderror and exit code
        """
        if not self._isConnectionActive():
            try:
                self.connect(connectionTimeout=connectionTimeout)
            except Exception as exception:
                LOGGER.error(
                    'Exception occurred while connecting ssh:' +
                    '\nCommand: {command}'.format(command=command) +
                    '\nException: {exception}'.format(exception=exception)
                )
                raise

        response = {
            'exitCode': None,
            'stdOut': None,
            'stdErr': None
        }

        try:
            tmpStdIn, tmpStdOut, tmpStdErr = self.connection.exec_command(
                command=command,
                timeout=executionTimeout,
                get_pty=True)
            stdOut = tmpStdOut.read()
            tmpExitCode = tmpStdOut.channel.recv_exit_status()
            response = {
                'exitCode': tmpExitCode,
                'stdOut': stdOut.decode('utf-8').strip(),
                'stdErr': tmpStdErr.read().decode('utf-8').strip()
            }
        except socket.timeout:
            LOGGER.error('Command execution timed out.' +
                         '\nCommand: {}'.format(command) +
                         '\nTimeout: {}'.format(executionTimeout))
            response = {
                'exitCode': errno.ETIME,
                'stdOut': None,
                'stdErr': None
            }
        except Exception as exception:
            LOGGER.error('Exception occurred while executing over ssh:' +
                         '\nCommand: {}'.format(command) +
                         '\nException: {}'.format(exception))
            raise

        return response

    def disconnect(self):
        """
        Disconnect the ssh connection.

        Guarantees:
            - No exception will be thrown even if the connection could not be
              closed.

        @return: None
        """
        try:
            if self.connection is not None:
                self.connection.close()
            self.connection = None
        except:
            pass  # do nothing

   
