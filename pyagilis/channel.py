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
from time import time,sleep
from datetime import datetime

RATE = 750
LIMSPEED = 3
TIMEOUT = 2000 

class Axis(object):
    
    def __init__(self,name = '1',stepAmp = 50,rate = RATE,controller = None):
        
        if controller == None:
            raise(ValueError('You cannot initialize an Axis without a controller'))
        self.controller = controller
        self.name = name
        self.rate = rate
        self.stepAmp = str(stepAmp) if 0<int(stepAmp)<=50 else str(50)
        self.controller.port.sendString(name+'SU+'+self.stepAmp+'\r\n')
        self.controller.port.sendString(name+'SU-'+self.stepAmp+'\r\n')
        
        self.__lastOp__ = 'opened'
    
    
    def whatDidIdo(self):
        
        return self.__lastOp__
    
    
    def stop(self):
        self.controller.port.sendString(self.name+'ST\n')
        self.__lastOp__ = 'stopped'
    
    
    def amIstill(self,rate):
        
        while True:
            if self.controller.port.sendString(self.name+'TS\n').find('0') != -1:
                return True
            sleep(0.001*rate)
            
            
    def amIatMyLimit(self):
        
        return self.controller.port.sendString('PH\n').find(self.name) != -1 or self.controller.port.sendString('PH\n').find('3') != -1
        
    
    def queryCounter(self):
        
        return int(self.controller.port.sendString(self.name+'TP\n')[3:])
    
    
    def resetCounter(self):
        
        self.controller.port.sendString(self.name+'ZP\n')
        self.__lastOp__ = 'reset'
        
    
    def jog(self,steps = 0):
        
        if steps == 0:
            return False
        
        self.__lastOp__ = 'jogged: '+str(steps)
        self.controller.port.sendString(self.name+'PR'+str(int(steps))+'\r\n')
    
    
    def goMax(self,speedTag = LIMSPEED):
        
        if self.__lastOp__ == 'goneMin':
            self.jog(500)
            self.amIstill(100)
        elif self.__lastOp__ == 'goneMax':
            return False 
            
        self.__lastOp__ = 'goneMax'
        self.controller.port.sendString(self.name+'MV'+str(speedTag)+'\r\n')
    
    
    def goMin(self,speedTag = LIMSPEED):
        
        if self.__lastOp__ == 'goneMax':
            self.jog(-500)
            self.amIstill(100)
        elif self.__lastOp__ == 'goneMin':
            return False
            
        self.__lastOp__ = 'goneMin'
        self.controller.port.sendString(self.name+'MV'+str(-1*speedTag)+'\r\n')
            
        
    def nowToMilliseconds(self):
        
        t = datetime.now()
        tMilli = t.microsecond/1000+t.second*1000+t.minute*60000+t.hour*3600000
        
        return tMilli
    
    
    def waitMe(self,interval):
        
        timePost = timePre = self.nowToMilliseconds()
        
        while timePost-timePre<interval:
            timePost = self.nowToMilliseconds()
        
