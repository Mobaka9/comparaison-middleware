import getopt
import os
import string
from ivy.std_api import *
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol



class IvyProtocol(AbstractProtocol):
    
    def __init__(self,args,logger,com):
        self.is_initialized = False
        self.args = args
        self.send_end = ""
        self.id = 0
        self.plt_data = []
        self.wait = True
        self.logger = logger
        self.pop_hello = True
        self.com = com
        self.client=""
        
    
    
   
        
    def initialize(self):
        
            if self.com == "PUB":
                IVYAPPNAME = 'Sender'

            else:
                IVYAPPNAME = 'Receiver'

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
            if self.com == "PUB":
                sleep(1)
                self.client = IvyGetApplication('Receiver')   

            self.is_initialized = True
            

    def send_message(self, message):
            #sleep(0.00001)
            #IvySendDirectMsg(self.client,1, message)
            IvySendMsg(message)
            
    @staticmethod
    def lprint(fmt, *arg):
            IVYAPPNAME = 'pyhello'
            print(IVYAPPNAME + ': ' + fmt % arg)

    def onmsgproc(self,agent, *larg):
        #self.lprint('Received from %r: [%s] ', agent, larg[1])
        t1= time.time()
        tmp = [self.id, larg[0], t1]
        self.plt_data.append(tmp)  
        self.id+=1

    def onmsgproc2(self, agent, *larg):
        t1= time.time()
        self.msg = larg[self.id]
        tmp = [self.id, larg[:50],t1, larg[-1]]
        self.plt_data.append(tmp)
        self.id+=1
        self.pop_hello = False
        
        
        
            
    def receive_message(self,message_count,queue,total_rec):
        #IvyBindDirectMsg(self.onmsgproc)
        IvyBindMsg(self.onmsgproc, '(.*)')
        #IvyBindMsg(self.onmsgproc2, 'flag0=(\S*) flag1=(\S*) flag2=(\S*) flag3=(\S*) flag4=(\S*) flag5=(\S*) flag6=(\S*) flag7=(\S*) flag8=(\S*) flag9=(\S*) flag10=(\S*) flag11=(\S*) flag12=(\S*) flag13=(\S*) flag14=(\S*) flag15=(\S*) flag16=(\S*) flag17=(\S*) flag18=(\S*) flag19=(\S*) flag20=(\S*) flag21=(\S*) flag22=(\S*) flag23=(\S*) flag24=(\S*) flag25=(\S*) flag26=(\S*) flag27=(\S*) flag28=(\S*) flag29=(\S*) flag30=(\S*) flag31=(\S*) flag32=(\S*) flag33=(\S*) flag34=(\S*) flag35=(\S*) flag36=(\S*) flag37=(\S*) flag38=(\S*) flag39=(\S*) flag40=(\S*) flag41=(\S*) flag42=(\S*) flag43=(\S*) flag44=(\S*) flag45=(\S*) flag46=(\S*) flag47=(\S*) flag48=(\S*) flag49=(\S*) flag50=(\S*) flag51=(\S*) flag52=(\S*) flag53=(\S*) flag54=(\S*) flag55=(\S*) flag56=(\S*) flag57=(\S*) flag58=(\S*) flag59=(\S*) flag60=(\S*) flag61=(\S*) flag62=(\S*) flag63=(\S*) flag64=(\S*) flag65=(\S*) flag66=(\S*) flag67=(\S*) flag68=(\S*) flag69=(\S*) flag70=(\S*) flag71=(\S*) flag72=(\S*) flag73=(\S*) flag74=(\S*) flag75=(\S*) flag76=(\S*) flag77=(\S*) flag78=(\S*) flag79=(\S*) flag80=(\S*) flag81=(\S*) flag82=(\S*) flag83=(\S*) flag84=(\S*) flag85=(\S*) flag86=(\S*) flag87=(\S*) flag88=(\S*) flag89=(\S*) flag90=(\S*) flag91=(\S*) flag92=(\S*) flag93=(\S*) flag94=(\S*) flag95=(\S*) flag96=(\S*) flag97=(\S*) flag98=(\S*) flag99=(\S*) flag100=(\S*) flag101=(\S*) flag102=(\S*) flag103=(\S*) flag104=(\S*) flag105=(\S*) flag106=(\S*) flag107=(\S*) flag108=(\S*) flag109=(\S*) flag110=(\S*) flag111=(\S*) flag112=(\S*) flag113=(\S*) flag114=(\S*) flag115=(\S*) flag116=(\S*) flag117=(\S*) flag118=(\S*) flag119=(\S*) flag120=(\S*) flag121=(\S*) flag122=(\S*) flag123=(\S*) flag124=(\S*) flag125=(\S*) flag126=(\S*) flag127=(\S*) flag128=(\S*) flag129=(\S*) flag130=(\S*) flag131=(\S*) flag132=(\S*) flag133=(\S*) flag134=(\S*) flag135=(\S*) flag136=(\S*) flag137=(\S*) flag138=(\S*) flag139=(\S*) flag140=(\S*) flag141=(\S*) flag142=(\S*) flag143=(\S*) flag144=(\S*) flag145=(\S*) flag146=(\S*) flag147=(\S*) flag148=(\S*) flag149=(\S*) flag150=(\S*) flag151=(\S*) flag152=(\S*) flag153=(\S*) flag154=(\S*) flag155=(\S*) flag156=(\S*) flag157=(\S*) flag158=(\S*) flag159=(\S*) flag160=(\S*) flag161=(\S*) flag162=(\S*) flag163=(\S*) flag164=(\S*) flag165=(\S*) flag166=(\S*) flag167=(\S*) flag168=(\S*) flag169=(\S*) flag170=(\S*) flag171=(\S*) flag172=(\S*) flag173=(\S*) flag174=(\S*) flag175=(\S*) flag176=(\S*) flag177=(\S*) flag178=(\S*) flag179=(\S*) flag180=(\S*) flag181=(\S*) flag182=(\S*) flag183=(\S*) flag184=(\S*) flag185=(\S*) flag186=(\S*) flag187=(\S*) flag188=(\S*) flag189=(\S*) flag190=(\S*) flag191=(\S*) flag192=(\S*) flag193=(\S*) flag194=(\S*) flag195=(\S*) flag196=(\S*) flag197=(\S*) flag198=(\S*) flag199=(\S*) #(\S*)')
        sleep(2)
        

        while(self.send_end != "LAST_MESSAGE"):
            #print(self.send_end)
            self.send_end = queue.get()
            print(self.send_end)

        print("here")
        if self.pop_hello:
            self.plt_data= self.plt_data[total_rec:]
        return self.plt_data
    
    def stopsocket(self):
        IvyStop()