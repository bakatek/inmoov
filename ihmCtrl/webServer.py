'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from storageCtrl import storageCtrl
if storageCtrl.getPlatformVersion() == 2:
    import SimpleHTTPServer
    import SocketServer
else:
    import http.server
    SimpleHTTPServer = http.server
    import socketserver
    SocketServer = socketserver

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        allCommands = storageCtrl.getAuthorizedCommands()
        for command in allCommands:
            splited = self.path.split("?")
            # if len(splited) > 1:
                # print("Command="+splited[0]+" =?= /www/"+command+" Params="+splited[1])
            if splited[0] == '/www/'+command:
                storageCtrl.pushWebRequest(splited[0], splited[1])
                # self.path = '/www/index.html'
                self.path = '/www/dummy.bmp'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        pass

class webServer(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("webServer:> "+_txt)

    def __init__(self, _utils_c, _port, _loopSleep):
        super(webServer,self).__init__()
        self.PORT = _port
        self.utils_c = _utils_c
        self.refreshRate = _loopSleep
        #self.webSrvHandler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.webSrvHandler = MyRequestHandler
        trys = 0
        connect = False
        while (connect == False) and (trys <99):
            try:
                self.httpd = SocketServer.TCPServer(("", self.PORT), self.webSrvHandler)
                connect = True
            except:
                self.out("Error binding http... try again.")
                sleep(2)
                trys = trys + 1
        
        self.out("init")
        
    def stop(self):
        self.httpd.server_close()
        self.out("stop")

    def run(self):
        storageCtrl.addThreadToStop(self)
        try:
            self.httpd.serve_forever()
        except:
            pass
        while storageCtrl.getStopRequested() == False:
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
