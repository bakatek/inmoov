'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from os import listdir
from os.path import isfile, join
import json
from time import sleep
from threading import Thread
from storageCtrl import storageCtrl
import pprint

class automation(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("automation:> "+_txt)

    def __init__(self, _utils_c, _hardwareThread, _loopSleep):
        super(automation,self).__init__()
        self.utils_c = _utils_c
        self.refreshRate = _loopSleep
        self.hardwareThread_l = _hardwareThread
        self.out("init")
        onlyfiles = [f for f in listdir(storageCtrl.getAutomationPath()) if isfile(join(storageCtrl.getAutomationPath(), f))]
        pprint.pprint(onlyfiles)
        for f in onlyfiles:
            with open(storageCtrl.getAutomationPath()+f) as data_file:
                try:
                    loaded_json = json.loads(data_file.read())
                    macro_l = {}
                    macro_l['name'] = f[:-5].lower()
                    macro_l['datas'] = loaded_json
                    storageCtrl.addAutomationMacro(macro_l)
                    storageCtrl.addAuthorizeMacro(macro_l['name'])
                except:
                    self.out("Error loading/parsing json "+f)
                    pass
                    
    def stop(self):
        self.out("stop")

    def run(self):
        storageCtrl.addThreadToStop(self)
        while storageCtrl.getStopRequested() == False:
            newReq = storageCtrl.getAutomationRequest()
            # print("GetAutomationReq")
            if newReq != None:
                
                self.out("REQ Automation  "+newReq)
                moveToDo = storageCtrl.getAutomationMacro(newReq)
                if moveToDo != None :
                    for i in moveToDo:
                        # print("i")
                        for j in i:
                            # print("j")
                            if j == 'move':
                                for k in i[j]: #each move in all moves
                                    # print("k")
                                    bodyPart = None
                                    part = None
                                    step = None
                                    mode = None
                                    for l in k: # a move
                                        # print("l")
                                        if l == "loc":
                                            bodyPart = k[l]
                                        elif l == "part":
                                            part = k[l]
                                        elif l == "pos":
                                            step = k[l]
                                        elif l == "mode":
                                            mode = k[l]
                                    if bodyPart != None and part != None and step != None and mode != None:
                                        self.hardwareThread_l.move(bodyPart, part, int(step), mode)
                            elif j == 'wait':
                                # print("wait "+str(i[j]))
                                sleep(int(i[j]))
                                
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
