import getopt
import os
import string
from ivy.std_api import *
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol



class IvyProtocol(AbstractProtocol):
    
    def __init__(self,args,logger):
        self.is_initialized = False
        self.args = args
        self.send_end = ""
        self.id = 0
        self.plt_data = []
        self.wait = True
        self.logger = logger
        self.pop_hello = True
        
    
    
   
        
    def initialize(self):
        if not self.is_initialized:
            IVYAPPNAME = 'pyhello'
            sivybus = ''
            sisreadymsg = '[%s is ready]' % IVYAPPNAME
            def lprint(fmt, *arg):

                print(IVYAPPNAME + ': ' + fmt % arg)

                
            def usage(scmd):
                lpathitem = string.split(scmd, '/')
                fmt = '''Usage: %s [-h] [-b IVYBUS | --ivybus=IVYBUS]
                where
                \t-h provides the usage message;
                \t-b IVYBUS | --ivybus=IVYBUS allow to provide the IVYBUS string in the form
                \t adresse:port eg. 127.255.255.255:2010
                '''
                print(fmt % lpathitem[-1])
            
            def oncxproc(agent, connected):
                if connected == IvyApplicationDisconnected:
                    lprint('Ivy application %r was disconnected', agent)
                else:
                    lprint('Ivy application %r was connected', agent)
                lprint('currents Ivy application are [%s]', IvyGetApplicationList())


            def ondieproc(agent, _id):
                lprint('received the order to die from %r with id = %d', agent, _id)

                    
            
            sivybus = self.args
            sechoivybus = sivybus
            lprint('Ivy will broadcast on %s ', sechoivybus)

                # initialising the bus
            IvyInit(IVYAPPNAME,     # application name for Ivy
                    sisreadymsg,    # ready message
                    0,              # main loop is local (ie. using IvyMainloop)
                    oncxproc,       # handler called on connection/disconnection
                    ondieproc)      # handler called when a <die> message is received
            IvyStart(sivybus)

            self.is_initialized = True
            

    def send_message(self, message):
            #sleep(0.00001)

            IvySendMsg(message)
            
    @staticmethod
    def lprint(fmt, *arg):
            IVYAPPNAME = 'pyhello'
            print(IVYAPPNAME + ': ' + fmt % arg)

    def onmsgproc(self,agent, *larg):
        #self.lprint('Received from %r: [%s] ', agent, larg[0])
        t1= time.time()
        self.msg = larg[0]
        #print(larg[0])
        tmp = [self.id, larg[0], t1]
        self.plt_data.append(tmp)  
        self.id+=1

    def onmsgproc2(self, agent, *larg):
        t1= time.time()
        self.msg = larg[self.id]
        tmp = [self.id, larg[:20],t1, larg[-1]]
        self.plt_data.append(tmp)
        self.id+=1
        self.pop_hello = False
        
        
        
            
    def receive_message(self,message_count,queue):
        print("bind")
        #IvyBindMsg(self.onmsgproc, '(.*)')
        IvyBindMsg(self.onmsgproc2, 'flag0=(\S*) flag1=(\S*) flag2=(\S*) flag3=(\S*) flag4=(\S*) flag5=(\S*) flag6=(\S*) flag7=(\S*) flag8=(\S*) flag9=(\S*) flag10=(\S*) flag11=(\S*) flag12=(\S*) flag13=(\S*) flag14=(\S*) flag15=(\S*) flag16=(\S*) flag17=(\S*) flag18=(\S*) flag19=(\S*) flag20=(\S*) flag21=(\S*) flag22=(\S*) flag23=(\S*) flag24=(\S*) flag25=(\S*) flag26=(\S*) flag27=(\S*) flag28=(\S*) flag29=(\S*) flag30=(\S*) flag31=(\S*) flag32=(\S*) flag33=(\S*) flag34=(\S*) flag35=(\S*) flag36=(\S*) flag37=(\S*) flag38=(\S*) flag39=(\S*) flag40=(\S*) flag41=(\S*) flag42=(\S*) flag43=(\S*) flag44=(\S*) flag45=(\S*) flag46=(\S*) flag47=(\S*) flag48=(\S*) flag49=(\S*) flag50=(\S*) flag51=(\S*) flag52=(\S*) flag53=(\S*) flag54=(\S*) flag55=(\S*) flag56=(\S*) flag57=(\S*) flag58=(\S*) flag59=(\S*) flag60=(\S*) flag61=(\S*) flag62=(\S*) flag63=(\S*) flag64=(\S*) flag65=(\S*) flag66=(\S*) flag67=(\S*) flag68=(\S*) flag69=(\S*) flag70=(\S*) flag71=(\S*) flag72=(\S*) flag73=(\S*) flag74=(\S*) flag75=(\S*) flag76=(\S*) flag77=(\S*) flag78=(\S*) flag79=(\S*) flag80=(\S*) flag81=(\S*) flag82=(\S*) flag83=(\S*) flag84=(\S*) flag85=(\S*) flag86=(\S*) flag87=(\S*) flag88=(\S*) flag89=(\S*) flag90=(\S*) flag91=(\S*) flag92=(\S*) flag93=(\S*) flag94=(\S*) flag95=(\S*) flag96=(\S*) flag97=(\S*) flag98=(\S*) flag99=(\S*) #(\S*)')
        queue.put("RECEIVER_READY")

        print(queue.get())
        while(self.send_end != "LAST_MESSAGE"):
            print(self.send_end)
            self.send_end = queue.get()
            print(self.send_end)

        
        if self.pop_hello:
            self.plt_data.pop(0)
        return self.plt_data
    
    def stopsocket(self):
        IvyStop()