#! /usr/bin/python

from twisted.internet import protocol, reactor
import datetime
from time import sleep

import os
import signal
import sys
import ConfigParser
import logging

#globals
log = logging.getLogger(__name__)
reactorPort = None

class AlveolusCore:
    """ Core controller class
    @TODO include adding co-operative multi threading and component
    registration - this will obviate the need for doing all of the
    imports in each of the file and will make code look cleaner
    """
    config = ConfigParser.ConfigParser()

    def __init__(self, configFile="controller.cfg"):
        retVal = self.config.read(configFile)
        getLogger()
        log.info('Initializing the controller.')

    def _configSectionMap(self, section):
        """ Create hash map for accessing configuration elements
        """
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except Exception, e:
                print("exception on %s!" % option)
                dict1[option] = None
                log.error('Failed to find section', exc_info=True)

        return dict1

class ListenerFactory(protocol.Factory):
    """ Twisted - setup the message handler 
    """
    def buildProtocol(self, addr):
        return self.msgHandler()
    
    def msgHandler():
        """ Message handler for incoming messages from clients
        """

def startListener(cConfig):
    """ Setup the listener
    """
    port = int(cConfig['port'])
    ip = cConfig['controllerip']
    reactorPort = reactor.listenTCP(port, ListenerFactory())
    log.info('Starting server on port [%s].' % port)
    reactor.run()

def signal_handler(signal, frame):
    log.info('Shutting down server.')
    if(reactorPort):
        reactorPort.stopListening()
    reactor.stop()

def getLogger():
    """ Setup logger for the module
    """
    # setting log config - TODO move it out to a config file
    log.setLevel(logging.INFO)
    logHandler = logging.FileHandler('alveolus.log')
    logHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler.setFormatter(formatter)
    log.addHandler(logHandler)


if __name__ == "__main__":
    """ Run the controller process 
    """

    '''TODO add parameters when starting the controller to specify custom
    configurations - for now using default config file
    '''
    signal.signal(signal.SIGINT, signal_handler)
    avCore = AlveolusCore()
    controllerConfig = avCore._configSectionMap("Controller")
    startListener(controllerConfig)

