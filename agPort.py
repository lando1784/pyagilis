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


import serial as s
from datetime import datetime

class AGPort(s.Serial):
    
    def __init__(self,portName = None):
        
        if portName == None:
            self.soul = None
            return None
        try:
            super(AGPort,self).__init__(portName,921600,s.EIGHTBITS,s.PARITY_NONE,s.STOPBITS_ONE)
            self.soul = 'p'
        except Exception as e:
            print e.message
            self.soul = None
            return None
    
        
    def amInull(self):
        return self.soul is None
    
    
    def isAquery(self,command):
        
        if self.amInull():
            return False
        
        queryOnly=["?","PH","TE","TP","TS","VE"]
        command = command.upper()
        for q in queryOnly:
            if command.find(q) != -1:
                return True
        return False
    
    
    def sendString(self,command):
        
        response = ''
        self.write(command)
        if self.isAquery(command):
            response = self.readline()
        return  response
            