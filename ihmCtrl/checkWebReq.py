'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from storageCtrl import storageCtrl

class checkWebReq(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("checkWebReq:> "+_txt)

    def __init__(self, _utils_c, _hardwareThread, _loopSleep):
        super(checkWebReq,self).__init__()
        self.utils_c = _utils_c
        self.refreshRate = _loopSleep
        self.hardwareThread_l = _hardwareThread
        self.out("init")
        
    def stop(self):
        self.out("stop")

    def run(self):
        storageCtrl.addThreadToStop(self)
        while storageCtrl.getStopRequested() == False:
            newReq = storageCtrl.getWebRequest()
            if newReq != None:
                self.out("REQ  "+newReq.command + " params="+newReq.params)
                if newReq.command == "/www/move":
                    tmpVal = newReq.params.split('|')
                    if len(tmpVal) > 1:
                        bodyPart = tmpVal[0]
                        part = tmpVal[1]
                        value = tmpVal[2]
                        if len(tmpVal) == 5:
                            mode = tmpVal[3]
                        else:
                            mode = 0
                        #print("TEST "+str(len(tmpVal))+ " mode:"+str(mode))
                        print("MOVE REQ "+str(bodyPart)+":"+str(part)+":"+str(value)+":"+str(mode))
                        self.hardwareThread_l.move(bodyPart, part, int(value), mode)
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
