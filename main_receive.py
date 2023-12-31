import zmq
from ivy.std_api import *
import sys
from abstract_protocol import AbstractProtocol
from ingescape_protocol import IngescapeProtocol
from zeromq import ZeroMQProtocol
from ivy_protocol import IvyProtocol
from kafka_protocol import KafkaProtocol
from message_analyzer import MessageReceiver
import multiprocessing

from time import sleep




def main_receive(protocol, message_count, port, length, queue, logger, flag, nmbre_rec, total_rec, multi_rec,direct_msg,device):
    
    
    com = "SUB"
    if protocol == 'ivy':
        protocol_obj = IvyProtocol(port, logger, com,None)
        protocol_obj.initialize()
    elif protocol == 'zeromq':
        port = int(port)
        #port +=1
        protocol_obj = ZeroMQProtocol(port, com,logger)
        protocol_obj.initialize()
    elif protocol == 'kafka':
        protocol_obj = KafkaProtocol(com,logger)
        protocol_obj.initialize()
    elif protocol == 'ingescape':
        protocol_obj = IngescapeProtocol(com,port,device,nmbre_rec,queue)
        protocol_obj.initialize()
    else:
        print("Unsupported protocol: "+str(protocol))
        return

    logger.info('Démarrage du receveur')

    #envoie de message aà l'autre process pour signaler que le receveur est prêt
    if(protocol != 'ingescape'):
        str_ready = "RECEIVER_READY "+str(nmbre_rec)
        queue.put(str_ready)
        print(f"receiver {nmbre_rec} pret")


        
        
    
    receiver = MessageReceiver(protocol_obj, protocol,length)
    receiver.receive_messages(message_count, queue, flag,nmbre_rec, total_rec, multi_rec,direct_msg)
    
    '''sender = MessageSender(protocol_obj)
    sender.send_messages(message_count)'''

