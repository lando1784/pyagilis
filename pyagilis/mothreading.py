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
#
# To implement this particular class I took this post  as a prototype: http://stackoverflow.com/questions/13125276/what-is-the-correct-way-to-make-a-stoppable-thread-in-python-given-stoppable



from threading import Thread


class MotorThread(Thread):
    
    stop_at_next_check = False
    
    def __init__(self,steps = []):
        
        super(MotorThread,self).__init__()
        self.steps = steps
    
    
    def execStep(self,step):
        if self.stop_at_next_check:
            return False
        step()
        
        return True
    
    
    def run(self):
        
        for s in self.steps:
            if not self.execStep(s):
                return None
