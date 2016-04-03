#!/usr/bin/python

from time import sleep

from storageCtrl import storageCtrl
from utils import utils
from ihmCtrl.checkWebReq import checkWebReq
from hardwareIO.hardwareIO import hardwareIO


if __name__ == '__main__':
    pass

def quitApp():
    storageCtrl.setStopRequested(True)
    while storageCtrl.getStopAcheived() > 0:
        utils_c.echo("waiting "+str(storageCtrl.getStopAcheived()),True)
        sleep(1)
    utils_c.echo("EXIT",True)

try:
    utils_c = utils()
    storageCtrl.init()
    storageCtrl.setUtils(utils_c)

    # here because storageCtrl init need to be complete
    from ihmCtrl.webServer import webServer
    # here because storageCtrl init need to be complete

    #if storageCtrl.getIsWindows() == True:
    if storageCtrl.DEBUG == True:
        #wait for GPIO init only for debug.
        sleep(1)
    
    hardwareIO_t = hardwareIO(utils_c, 0.1)
    hardwareIO_t.start()
    
    webServer_t = webServer(utils_c,80,0.1)
    webServer_t.start()
    
    checkWebReq_t = checkWebReq(utils_c, hardwareIO_t, 0.1)
    checkWebReq_t.start()
    
    
    utils_c.echo("************************************************************************",True)
    try:
        if platform.python_version().find("3.") != -1:
            raw_input = input
    except:
        pass
    inputKeyb = raw_input('Press "q" to Quit: ')
    while True and storageCtrl.getStopRequested()==False:
        if inputKeyb == "q":
            storageCtrl.setStopRequested(True)
            for i in storageCtrl.getThreadsToStop():
                i.stop()
        sleep(1)
    
except KeyboardInterrupt:
    quitApp()


