'''
Created on 15 dec. 2015
@author: epelorce
'''

import os
from time import sleep
from threading import Thread
from storageCtrl import storageCtrl
from Adafruit_PWM_Servo_Driver import PWM

class actionMove:
    def __init__(self, _part, _move, _mode, _forceRefresh, _interface, _port):
        print("_part:"+str(_part)+" _move:"+str(_move)+" _mode:"+str(_mode)+" _forceRefresh:"+str(_forceRefresh)+" _interface:"+str(_interface)+" _port:"+str(_port))
        self.part = _part
        self.move = int(_move)
        self.mode = int(_mode)
        self.interface = int(_interface)
        self.forceRefresh = _forceRefresh
        self.port = int(_port)
    
    def getPart(self):
        return self.part
        
    def getMove(self):
        return self.move
        
    def getMode(self):
        return self.mode
        
    def getInterface(self):
        return self.interface
        
    def getForceRefresh(self):
        return self.forceRefresh
        
    def getPort(self):
        return self.port
        
class interface:
    def __init__(self, _name, _i2c_add):
        #print("init interface")
        self.name = _name
        self.i2c_add = _i2c_add
        self.conf = []

    def addMotor(self, _motor):
        self.conf.append(_motor)

class motor:    
    def __init__(self, _utils_c, _motorType, _bodyPart, _name, _position, _mode, _timing, _reverseMode = False):
        self.utils_c = _utils_c
        self.motorType = _motorType
        self.bodyPart = _bodyPart
        self.name = _name
        self.position = _position
        self.reverseMode = _reverseMode
        self.mode = _mode
        self.mode_timing = _timing
        self.motor_t = motorThread(self.utils_c, self, 0.1)
        self.motor_t.start()

class motorThread(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("motorThread:> "+_txt)

    def __init__(self, _utils_c, _motor_c, _loopSleep):
        super(motorThread, self).__init__()
        self.utils_c = _utils_c
        self.refreshRate = _loopSleep
        self.motor_c = _motor_c
        self.actions = []
        self.out("init")

    def stop(self):
        self.out("stop")

    def moveServo(self, _interface, _port, _move, _forceRefresh = False):
        if _move != INTERFACES_CONFIGURATION[_interface].conf[_port].position or _forceRefresh == True:
                    maxPulse = globals()["MAX_PULSE_"+INTERFACES_CONFIGURATION[_interface].conf[_port].motorType]
                    minPulse = globals()["MIN_PULSE_"+INTERFACES_CONFIGURATION[_interface].conf[_port].motorType]
                    pulse = ((_move*(maxPulse-minPulse))/ 100) + minPulse
                    INTERFACES_CONFIGURATION[_interface].instance.setPWM(_port, 0, pulse)
                    INTERFACES_CONFIGURATION[_interface].conf[_port].position = _move
                    
    def move(self, _interface, _port, _move, _mode, _forceRefresh = False):
        #self.out("Move interface:"+str(_interface)+" port:"+str(_port)+" move:"+str(_move)+" force:"+str(_forceRefresh))
        if INTERFACES_CONFIGURATION[_interface].conf[_port].reverseMode == True:
            _move = 100 - _move
        if (_interface != -1) and (_port != -1) and (_move >= 0) and (_move <= 100):
            self.moveServo(_interface, _port, _move, _forceRefresh)
        elif _move == -1:
            INTERFACES_CONFIGURATION[_interface].instance.setPWM(_port, 0, 0)
        else:
            self.out("Do Nothing")

        print("-----> MODE !!! "+str(_mode))
        if int(_mode) == 1 :
            sleep(INTERFACES_CONFIGURATION[_interface].conf[_port].mode_timing)
            INTERFACES_CONFIGURATION[_interface].instance.setPWM(_port, 0, 0)
            sleep(INTERFACES_CONFIGURATION[_interface].conf[_port].mode_timing)
            self.moveServo(_interface, _port, _move, _forceRefresh)
        elif int(_mode) == 2 :
            sleep(INTERFACES_CONFIGURATION[_interface].conf[_port].mode_timing)
            INTERFACES_CONFIGURATION[_interface].instance.setPWM(_port, 0, 0)
            self.moveServo(_interface, _port, _move, True)
            sleep(INTERFACES_CONFIGURATION[_interface].conf[_port].mode_timing)
            INTERFACES_CONFIGURATION[_interface].instance.setPWM(_port, 0, 0)
        elif int(_mode) == 3 :
            sleep(1)
            self.moveServo(_interface, _port, _move, True)
            sleep(1)
            INTERFACES_CONFIGURATION[_interface].instance.setPWM(_port, 0, 0)
            sleep(1)
            self.moveServo(_interface, _port, _move, True)

    def getAct(self):
        if len(self.actions) > 0:
            return self.actions.pop()
        else:
            return None

    def addAct(self, _action):
        self.actions.append(_action)

    def run(self):
        storageCtrl.addThreadToStop(self)
        while storageCtrl.getStopRequested() == False:
            sleep(self.refreshRate)
            local_act = self.getAct()
            if local_act != None:
                self.move(local_act.getInterface(), local_act.getPort(), local_act.getMove(),local_act.getMode(), local_act.getForceRefresh())
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1

class robot:
    def __init__(self, _utils_c):
        print("Starting")
        interface0 = interface("interface0", 0X40)
        #_motorType, _bodyPart, _name, _position, _mode, _timing, _reverseMode = False
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "thumb", 50,2,0.5, False))
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "forefinger", 50,2,0.5, False))
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "middlefinger", 50,2,0.5, False))
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "ringfinger", 50,2,0.5, False))
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "smallfinger", 50,2,0.5, False))
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "wrist", 50,1,0.5, False))
        interface0.addMotor(motor(_utils_c, "HITEC805BBelbw", "LEFT_ARM", "elbow", 27,2,1.5,True))
        interface0.addMotor(motor(_utils_c, "HKSHOULDERa", "LEFT_ARM", "shoulder_A", 50,0,1.5, True))
        interface0.addMotor(motor(_utils_c, "QS40KG", "LEFT_ARM", "shoulder_B", 50,0,2.5, True))
        interface0.addMotor(motor(_utils_c, "HKFINGER", "LEFT_ARM", "shoulder_Blade", 50,0,0.5, False))
        
        INTERFACES_CONFIGURATION.append(interface0)
        
        # Initialise the PWM device using the default address
        for i in range(0,len(INTERFACES_CONFIGURATION)):
            print("INIT I2C interfaces "+str(i)+" "+INTERFACES_CONFIGURATION[i].name+" Add:"+str(INTERFACES_CONFIGURATION[i].i2c_add)+"\n")
            try:
                INTERFACES_CONFIGURATION[i].instance = PWM(INTERFACES_CONFIGURATION[i].i2c_add)
            except:
                print("ERROR in init i2c_add")
                pass

    def moveTopLvl(self, _bodyPart, _part, _move, _mode, _forceRefresh = False):
        _move = int(_move)
        #print("TOP LVL MOVE body:"+str(_bodyPart)+" part:"+str(_part)+" move:"+str(_move)+" mode:"+str(_mode)) 
        config = self.getInterfaceAndPort(_bodyPart, _part)
        INTERFACES_CONFIGURATION[config[0]].conf[config[1]].motor_t.addAct(actionMove(_part,_move, _mode, _forceRefresh, config[0], config[1]))

    def getInterfaceAndPort(self, bodyPart, name):
        i = -1
        j = -1
        for i in range(0,len(INTERFACES_CONFIGURATION)):
            # interface loop
            for j in range(0,len(INTERFACES_CONFIGURATION[i].conf)):
                #each port loop
                if (bodyPart == INTERFACES_CONFIGURATION[i].conf[j].bodyPart) and (name == INTERFACES_CONFIGURATION[i].conf[j].name):
                    return [i,j]
        return [-1,-1]

    def init(self):
        print("init pwm")
        for i in range(0,len(INTERFACES_CONFIGURATION)):
            for j in range(0, len(INTERFACES_CONFIGURATION[i].conf)):
                bodyPart_l = INTERFACES_CONFIGURATION[i].conf[j].bodyPart
                part_l = INTERFACES_CONFIGURATION[i].conf[j].name
                self.moveTopLvl(bodyPart_l, part_l , INTERFACES_CONFIGURATION[i].conf[j].position, INTERFACES_CONFIGURATION[i].conf[j].mode, True)
                print("INIT "+bodyPart_l+ " "+ part_l+ " => "+str(INTERFACES_CONFIGURATION[i].conf[j].position))
        return

INTERFACES_CONFIGURATION = []

## HK finger Section
MAX_PULSE_HKFINGER = 2070
MIN_PULSE_HKFINGER = 526
## HK finger Section

## HITEC805BB finger Section
# MAX_PULSE_HITEC805BBelbw = 1200
MAX_PULSE_HITEC805BBelbw = 1200
MIN_PULSE_HITEC805BBelbw = 485
## HITEC805BB finger Section
# MAX_PULSE_HITEC805BBelbw = 1200
MAX_PULSE_HITEC805BB = 1300
MIN_PULSE_HITEC805BB = 485
## HITEC805BB finger Section

## HK shoulder Section
MAX_PULSE_HKSHOULDERa = 2000
MIN_PULSE_HKSHOULDERa = 546
## HK shoulder Section

## HK shoulder Section
MAX_PULSE_QS40KG = 2070
MIN_PULSE_QS40KG = 540
## HK shoulder Section

class hardwareIO(Thread):
    '''
    classdocs
    '''

    def out(self, _txt):
        self.utils_c.echo("hardwareIO:> "+_txt)

    def __init__(self, _utils_c, _loopSleep):
        super(hardwareIO,self).__init__()
        self.utils_c = _utils_c
        self.refreshRate = _loopSleep
        self.out("init")

    def stop(self):
        self.out("stop")

    def move(self, _bodyPart, _part, _value, _mode):
        self.robot.moveTopLvl(_bodyPart, _part, _value, _mode)

    def run(self):
        storageCtrl.addThreadToStop(self)
        self.robot = robot(self.utils_c)
        self.robot.init()
        while storageCtrl.getStopRequested() == False:
            sleep(self.refreshRate)
        storageCtrl.stopAcheived = storageCtrl.getStopAcheived() - 1
