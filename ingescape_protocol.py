
import sys
import ingescape as igs
import getopt
import os
import string
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol

def string_input_callback(iop_type, iop_name, value_type, value, my_data):
    #igs.output_set_int("out", value)
    #igs.info(f"received {value}")
    callback_self = my_data
    if isinstance(callback_self,IngescapeProtocol):
        #print("hey")
        t1= time.time()
        tmp = [callback_self.id, value, t1]
        callback_self.plt_data.append(tmp) 
        #print(f"{callback_self.id_rec}receiving message number {callback_self.id}") 
        callback_self.id+=1
    else:
        print("error callback_self")

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    callback_self=my_data
    if isinstance(callback_self,IngescapeProtocol):
        
        if event == igs.PEER_ENTERED:
            print(f"PEER_ENTERED about {name}")
        elif event == igs.PEER_EXITED:
            print(f"PEER_EXITED about {name}")
        elif event == igs.AGENT_ENTERED:
            print(f"AGENT_ENTERED about {name}")
        elif event == igs.AGENT_UPDATED_DEFINITION:
            print(f"AGENT_UPDATED_DEFINITION about {name}")
        elif event == igs.AGENT_KNOWS_US:
            print(f"AGENT_KNOWS_US about {name}")
            #if callback_self =="SUB":
                
        elif event == igs.AGENT_EXITED:
            print(f"AGENT_EXITED about {name}")
        elif event == igs.AGENT_UPDATED_MAPPING:
            print(f"AGENT_UPDATED_MAPPING about {name}")
        elif event == igs.AGENT_WON_ELECTION:
            print(f"AGENT_WON_ELECTION about {name}")
        elif event == igs.AGENT_LOST_ELECTION:
            print(f"AGENT_LOST_ELECTION about {name}")
        else:
            print(f"UNKNOWN event about {name}")
    else:
        print("error callback event")

class IngescapeProtocol(AbstractProtocol):
    
    def __init__(self,com,port,device,id_rec):
        self.is_initialized = False
        self.port = port
        self.send_end = ""
        self.id = 0
        self.plt_data = []
        self.wait = True
        self.device=device
        self.com = com
        self.client=""
        self.id_rec=id_rec

        
        
    def initialize(self):
        
            if self.com == "PUB":
                IGSAPPNAME = 'Sender'

            else:
                IGSAPPNAME = 'Receiver '+str(self.id_rec)

            
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
            igs.observe_agent_events(on_agent_event_callback, self)
            igs.net_set_high_water_marks(0)
            #igs.net_raise_sockets_limit()
            
            
            if self.com=="PUB":
                igs.output_create("out", igs.STRING_T, None)
            else:
                igs.input_create("in", igs.STRING_T, None)
                igs.observe_input("in", string_input_callback, self)
                igs.mapping_add("in", "Sender", "out")
            
            igs.start_with_device(self.device, int(self.port))


            self.is_initialized = True
            

    def send_message(self, message):
            #sleep(0.00001)
            #IvySendDirectMsg(self.client,1, message)
            igs.output_set_string("out", message)
    
    

    def receive_message(self,message_count,queue,total_rec,direct_msg,flag):
            

        #sleep(5)
        
        while len(self.plt_data) != message_count:
            pass 
        if self.id_rec==0:
            print("hey 0")
            queue.put("close_sock")
        else:
            print("hey 1")  
        print("close sent by rcv for snd")
        # print(self.plt_data)
        # print(len(self.plt_data))

        # while(self.send_end != "LAST_MESSAGE"):
        #     print(self.send_end)
        #     self.send_end = queue.get()
        #     print(self.send_end)
        return self.plt_data
    
    def stopsocket(self):
        print(f"trying to close {self.com}")
        igs.stop()
        