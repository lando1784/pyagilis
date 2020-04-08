#
# Copyright (C) 2015-2016 Ettore Landini
#
# This code is translated from another project of mines written in C#
#
# This is a python library for the NewPort Agilis controlle agUC2 and agUC8
#
# You can find another approach to this problem here: http://nullege.com/codes/show/src@t@e@terapy-2.00b6
#
#
#

## @package agPort
# This module contain classes that implements custom versions of python built-in serial port class
# for the agilis controllers 
#

from datetime import datetime

import serial as s


## Documentation for the AGPort class
#
# This class extend the python Serial class with some function that simplifies its use with the agilis controllers commands
class AGPort(s.Serial):
    
    ## Class constructor
    # @param portName String: The name of the virtual serial port of the chosen controller
    # @param testRead Boolean: If true when reading it will read byte by byte and print the result (for a maximum of 16 bytes)
    def __init__(self,portName = None, testRead = False):
        
        if portName == None:
            ## @var AGPort.soul
            self.soul = None
            return
        try:
            super(AGPort,self).__init__(portName,921600,s.EIGHTBITS,s.PARITY_NONE,s.STOPBITS_ONE)
            self.soul = 'p'
        except Exception as e:
            print('I could not find or open the port you specified: {0}'.format(portName))
            self.soul = None
            return
        self._testRead = testRead
    
    ## Checks if the port has been successfully opened
    def amInull(self):
        return self.soul is None
    
    ## Checks whether the string you sent is supposed to get an answer or not
    # @param command The string you want to send to the serial port
    def isAquery(self,command):
        
        if self.amInull():
            return False
        
        queryOnly=["?","PH","TE","TP","TS","VE"]
        command = command.upper()
        for q in queryOnly:
            if command.find(q) != -1:
                return True
        return False
    
    ## Sends the command you want to the port and, if it's supposed to get an answer it returns the response
    # @params command The string you want to send to the serial port
    def sendString(self,command):
        
        response = ''
        bCommand = bytes(command,'UTF-8')
        self.write(bCommand)
        if self.isAquery(command):
            if not self._testRead:
                response = self.readline().decode('utf-8')
            else:
                for i in range(16):
                    try:
                        x = self.read(1).decode('utf-8')
                        print(x)
                    except Exception as e:
                        print(e)
                return ""
        return response
