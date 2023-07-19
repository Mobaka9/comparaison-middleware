
import sys
import ingescape as igs
import getopt
import os
import string
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol



class IngescapeProtocol(AbstractProtocol):
    
    def __init__(self,com,port,device):
        self.is_initialized = False
        self.port = port
        self.send_end = ""
        self.id = 0
        self.plt_data = []
        self.wait = True
        self.device=device
        self.com = com
        self.client=""
        
    
    
    def string_input_callback(self,iop_type, iop_name, value_type, value, my_data):
        #igs.output_set_int("out", value)
        print("callback")
        igs.info(f"received {value}")
        t1= time.time()
        print("callback")
        tmp = [self.id, value, t1]
        self.plt_data.append(tmp)  
        self.id+=1
    def on_agent_event_callback(event, uuid, name, event_type, my_data):

        if event_type == igs.PEER_ENTERED:

            print("PEER_ENTERED")

        elif event_type == igs.PEER_EXITED:

            print("PEER_EXITED")

        elif event_type == igs.AGENT_ENTERED:

            print("AGENT_ENTERED")

        elif event_type == igs.AGENT_UPDATED_DEFINITION:

            print("AGENT_UPDATED_DEFINITION")

        elif event_type == igs.AGENT_KNOWS_US:

            print("AGENT_KNOWS_US")

        elif event_type == igs.AGENT_EXITED:

            print("AGENT_EXITED")
        elif event_type == igs.AGENT_UPDATED_MAPPING:

            print("AGENT_UPDATED_MAPPING")

        elif event_type == igs.AGENT_WON_ELECTION:

            print("AGENT_WON_ELECTION")

        elif event_type == igs.AGENT_LOST_ELECTION:

            print("AGENT_LOST_ELECTION")

        else:

            print("UNKNOWN")
        
    def initialize(self):
        
            if self.com == "PUB":
                IGSAPPNAME = 'Sender'

            else:
                IGSAPPNAME = 'Receiver'

            
            # def oncxproc(agent, connected):
            #     if connected == IvyApplicationDisconnected:
            #         lprint('Ivy applicatio)n %r was disconnected', agent)
            #     else:
            #         lprint('Ivy applicatio)n %r was connected', agent)
            #     lprint('currents Ivy a)pplication are [%s]', IvyGetApplicationList())


            # def ondieproc(agent, _id):
            #     lprint('received the o)rder to die from %r with id = %d', agent, _id)

            print(f'Ingescape {IGSAPPNAME} will communicate on device {self.device} and port {self.port}')
            igs.agent_set_name(IGSAPPNAME)
            igs.log_set_console(True)
            igs.log_set_file(True, None)
            igs.definition_set_version("1.0")
            igs.observe_agent_events(self.on_agent_event_callback, None)
            
            if self.com=="PUB":
                igs.output_create("out", igs.STRING_T, None)
            else:
                igs.input_create("in", igs.STRING_T, None)
                igs.observe_input("in", self.string_input_callback, None)
                igs.mapping_add("in", "Sender", "out")
            
            igs.start_with_device(self.device, int(self.port))


            self.is_initialized = True
            

    def send_message(self, message):
            #sleep(0.00001)
            #IvySendDirectMsg(self.client,1, message)
            igs.output_set_string("out", message)
    
    

    def receive_message(self,message_count,queue,total_rec,direct_msg,flag):
            

        #sleep(5)
        print("hello")
        print(self.plt_data)
        while self.id!=5:
            pass   
        print(self.plt_data)

        # while(self.send_end != "LAST_MESSAGE"):
        #     print(self.send_end)
        #     self.send_end = queue.get()
        #     print(self.send_end)

        # if not direct_msg:
        #     if self.pop_hello:
        #         self.plt_data= self.plt_data[total_rec:]
        # print(self.plt_data
    
    def stopsocket(self):
        # igs.stop()
        print("stop socket ingescape")
        pass