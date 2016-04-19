'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
import platform

class webCommand:
    
    def __init__(self, _command, _params):
        self.command = _command
        self.params = _params
        

class storageCtrl(object):
    '''
    classdocs
    '''
    @staticmethod
    def init():
        '''
        Constructor
        '''
        storageCtrl.Version = "0.0.0.1"
        storageCtrl.DEBUG = True
        storageCtrl.verboseLevel = 1
        storageCtrl.platformVersion = -1
        
        storageCtrl.authorizedCommands = ["finger", "move"]
        
        
        storageCtrl.keyboardManagerThread = None
        storageCtrl.threadToStop = []
        storageCtrl.fingerMoveReq = []
        storageCtrl.webRequests = []
        storageCtrl.authorizedMacros = []
        storageCtrl.stopAcheived = 0
        storageCtrl.stopRequested = False
        storageCtrl.setStopAcheived = False
        storageCtrl.automationMacros = {}
        storageCtrl.automationPath = "./automation/datas/"
        storageCtrl.automationRequests = []
        
        if platform.python_version().find("3.") != -1:
            storageCtrl.setPlatformVersion(3)
        else:
            storageCtrl.setPlatformVersion(2)
            
    
    @staticmethod
    def pushAutomationRequest(_macro):
        # print("pushAutomationRequest" + _macro)
        storageCtrl.automationRequests.append(_macro)
    
    @staticmethod
    def getAutomationRequest():
        # print("getAutomationRequest")
        # pprint.pprint(storageCtrl.automationRequests)
        if len(storageCtrl.automationRequests) > 0:
            return storageCtrl.automationRequests.pop(0)
        else:
            return None
    
            
            
    @staticmethod
    def addAutomationMacro(_addMacro):
        print("AddMacro "+_addMacro['name'])
        storageCtrl.automationMacros[_addMacro['name']] = _addMacro['datas']
        for i in storageCtrl.automationMacros:
            print("Check "+i)

    @staticmethod
    def getAutomationMacro(_macroName):
        print("getAutomationMacro "+_macroName)
        try:
            return storageCtrl.automationMacros[_macroName]
        except:
            return None
            
    @staticmethod
    def getAutomationPath():
        return storageCtrl.automationPath
            
    @staticmethod
    def addThreadToStop(_addThread):
        storageCtrl.threadToStop.append(_addThread)
        
    @staticmethod
    def getThreadsToStop():
        return storageCtrl.threadToStop
            
    @staticmethod
    def getThreadToStop():
        if len(storageCtrl.threadToStop) > 0:
            return storageCtrl.threadToStop.pop()
        else:
            return None
    
    @staticmethod
    def setPlatformVersion(_platformVersion):
        storageCtrl.platformVersion = _platformVersion

    @staticmethod
    def getPlatformVersion():
        return storageCtrl.platformVersion

    @staticmethod
    def getAuthorizedCommands():
        return storageCtrl.authorizedCommands

    @staticmethod
    def getAuthorizedMacros():
        return storageCtrl.authorizedMacros
        
    @staticmethod
    def addAuthorizeMacro(_macro):
        storageCtrl.authorizedMacros.append(_macro)
    

    @staticmethod
    def pushWebRequest(_command, _params):
        storageCtrl.webRequests.append(webCommand(_command,_params))
    
    @staticmethod
    def getWebRequest():
        if len(storageCtrl.webRequests) > 0:
            return storageCtrl.webRequests.pop(0)
        else:
            return None
    
    @staticmethod
    def getVersion():
        return storageCtrl.Version
    
    @staticmethod
    def isWINDOWS():
        return storageCtrl.ISWINDOWS
    
    @staticmethod
    def getLocalPath():
        return storageCtrl.LocalPath
    
    @staticmethod
    def setStopAcheived(_datas):
        storageCtrl.stopAcheived = _datas

    @staticmethod
    def getStopAcheived():
        return storageCtrl.stopAcheived

    @staticmethod
    def setUtils(_utils_c):
        storageCtrl.utils_c = _utils_c

    @staticmethod
    def setStopRequested(_datas):
        storageCtrl.stopRequested = _datas
    
    @staticmethod
    def getStopRequested():
        return storageCtrl.stopRequested       
    
    @staticmethod
    def getIsWindows():
        if os.name == "nt":
            return True
        else:
            return False
