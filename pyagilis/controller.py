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

from .agPort import AGPort
from .channel import RATE, Axis
from .mothreading import MotorThread


class AGUC2(object):
    
    def __init__(self,portName, axis1alias = 'X', axis2alias = 'Y', stepAmp1 = 50, stepAmp2 = 50):
        
        self.port = AGPort(portName)
        self.axis = {}
        
        self.aliases = [axis1alias,axis2alias]
        
        self.mThread = MotorThread()
        
        if not self.port.amInull():
            self.port.sendString('MR\r\n')
            self.addAxis('1',axis1alias,stepAmp1)
            self.addAxis('2',axis2alias,stepAmp2)
        
        
    def addAxis(self,name,alias,stepAmp):
        
        self.axis[alias] = Axis(name,stepAmp,controller = self)
    
    
    def move(self,d1,d2):
        
        self.axis[self.aliases[0]].jog(d1)
        self.axis[self.aliases[0]].amIstill(100)
        self.axis[self.aliases[1]].jog(d2)
        self.axis[self.aliases[1]].amIstill(100)
        
    
    def moveUpUp(self):
        
        self.axis[self.aliases[0]].goMax()
        self.axis[self.aliases[0]].amIstill(RATE)
        self.axis[self.aliases[1]].goMax()
        self.axis[self.aliases[1]].amIstill(RATE)
        
        
    def moveDownDown(self):
        
        self.axis[self.aliases[0]].goMin()
        self.axis[self.aliases[0]].amIstill(RATE)
        self.axis[self.aliases[1]].goMin()
        self.axis[self.aliases[1]].amIstill(RATE)
        
        
    def moveDownUp(self):
        
        self.axis[self.aliases[0]].goMin()
        self.axis[self.aliases[0]].amIstill(RATE)
        self.axis[self.aliases[1]].goMax()
        self.axis[self.aliases[1]].amIstill(RATE)
        
        
    def moveUpDown(self):
        
        self.axis[self.aliases[0]].goMax()
        self.axis[self.aliases[0]].amIstill(RATE)
        self.axis[self.aliases[1]].goMin()
        self.axis[self.aliases[1]].amIstill(RATE)
        
        
    def goToZero(self):
        
        steps1 = self.axis[self.aliases[0]].queryCounter()
        steps2 = self.axis[self.aliases[1]].queryCounter()
        
        self.axis[self.aliases[0]].jog(-1*steps1)
        self.axis[self.aliases[0]].amIstill(150)
        self.axis[self.aliases[1]].jog(-1*steps2)
        self.axis[self.aliases[1]].amIstill(150)
        
    
    def setZero(self):
        
        self.axis[self.aliases[0]].resetCounter()
        self.axis[self.aliases[1]].resetCounter()
        
        
    def stop(self):
        
        if self.mThread.isAlive():
            self.mThread.stop_at_next_check = True
            while self.mThread.isAlive():
                continue
            self.mThread = MotorThread()
        self.axis[self.aliases[0]].stop()
        self.axis[self.aliases[1]].stop()
        
    
    def followApath(self,path):
        
        steps = []
        for p in path:
            step = lambda: self.move(p[0], p[1])
            steps.append(step)
        self.mThread.steps = steps
        self.mThread.start()
            
        

class AGUC8(object):
    
    def __init__(self,portName,activeChannels = ['1'], axis1alias = 'X', axis2alias = 'Y', stepAmp1 = 50, stepAmp2 = 50):
        
        self.port = AGPort(portName)
        self.channels = {'1':{axis1alias:None,axis2alias:None},
                         '2':{axis1alias:None,axis2alias:None},
                         '3':{axis1alias:None,axis2alias:None},
                         '4':{axis1alias:None,axis2alias:None}}
        
        self.aliases = [axis1alias,axis2alias]
        
        self.defChannel = activeChannels[0]
        
        if not self.port.amInull():
            self.port.sendString('MR\r\n')
            for c in activeChannels:
                self.port.sendString('CC'+str(c)+'\r\n')
                self.addAxis(c,'1',axis1alias,stepAmp1)
                self.addAxis(c,'2',axis2alias,stepAmp2)
            self.port.sendString('CC'+str(activeChannels[0])+'\r\n')
            self.mThread = MotorThread()
        
        
    def chchch(self,ch):
        
        #CHeck and CHange CHannel
        
        channel = int(self.port.sendString('CC?\r\n')[2:])
        if channel != ch:
            self.port.sendString('CC'+str(ch)+'\r\n')
        
        
    def addAxis(self,channel,name,alias,stepAmp):
        
        if alias not in self.aliases:
            raise KeyError('You used an invalid axis name')
        self.channels[channel][alias] = Axis(name,stepAmp,controller = self)
    
    
    def move(self,d1,d2,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        self.channels[ch][self.aliases[0]].jog(d1)
        self.channels[ch][self.aliases[0]].amIstill(100)
        self.channels[ch][self.aliases[1]].jog(d2)
        self.channels[ch][self.aliases[1]].amIstill(100)
        
    
    def moveUpUp(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        self.channels[ch][self.aliases[0]].goMax()
        self.channels[ch][self.aliases[0]].amIstill(RATE)
        self.channels[ch][self.aliases[1]].goMax()
        self.channels[ch][self.aliases[1]].amIstill(RATE)
        
        
    def moveDownDown(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        self.channels[ch][self.aliases[0]].goMin()
        self.channels[ch][self.aliases[0]].amIstill(RATE)
        self.channels[ch][self.aliases[1]].goMin()
        self.channels[ch][self.aliases[1]].amIstill(RATE)
        
        
    def moveDownUp(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        self.channels[ch][self.aliases[0]].goMin()
        self.channels[ch][self.aliases[0]].amIstill(RATE)
        self.channels[ch][self.aliases[1]].goMax()
        self.channels[ch][self.aliases[1]].amIstill(RATE)
        
        
    def moveUpDown(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        self.channels[ch][self.aliases[0]].goMax()
        self.channels[ch][self.aliases[0]].amIstill(RATE)
        self.channels[ch][self.aliases[1]].goMin()
        self.channels[ch][self.aliases[1]].amIstill(RATE)
        
        
    def goToZero(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        steps1 = self.channels[ch][self.aliases[0]].queryCounter()
        steps2 = self.channels[ch][self.aliases[1]].queryCounter()
        
        self.channels[ch][self.aliases[0]].jog(-1*steps1)
        self.channels[ch][self.aliases[0]].amIstill(150)
        self.channels[ch][self.aliases[1]].jog(-1*steps2)
        self.channels[ch][self.aliases[1]].amIstill(150)
        
    
    def setZero(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        self.channels[ch][self.aliases[0]].resetCounter()
        self.channels[ch][self.aliases[1]].resetCounter()
        
        
    def stop(self,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        if self.mThread.isAlive():
            self.mThread.stop_at_next_check = True
            while self.mThread.isAlive():
                continue
            self.mThread = MotorThread()
        self.channels[ch][self.aliases[0]].stop()
        self.channels[ch][self.aliases[1]].stop()
        
    
    def followApath(self,path,ch='def'):
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        steps = []
        for p in path:
            step = lambda: self.move(ch,p[0], p[1])
            steps.append(step)
        self.mThread.steps = steps
        self.mThread.start()
