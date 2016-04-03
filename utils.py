'''
Created on 15 dec. 2015
@author: epelorce
'''

import random
import uuid
import time
from storageCtrl import storageCtrl
from string import Template
from os import listdir
from os import path

    
class utils(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.storageCtrl_t = storageCtrl

    def echo(self, _txt, _force=False, _verboseLvl=0):
        if  len(_txt) > 0 and self.storageCtrl_t.DEBUG == True and self.storageCtrl_t.verboseLevel >= _verboseLvl:
            print("Debug-> "+_txt)
        elif  len(_txt) > 0 and _force == True:
            print(_txt)

    def fileExist(self, _path):
        return path.isfile(_path)
        

    def writeBinaryFile(self, _path, _data):
        newFileByteArray = bytearray(_data)
        newfile=open(_path,'wb')
        newFile.write(newFileByteArray)
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
     
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
     
        return False
    
    def saveFile(self, _datas, _filename):
        length = len(_datas)
        with open(self.storageCtrl_t.getStorePath()+_filename, 'wb') as fh:
            fh.write(_datas)
