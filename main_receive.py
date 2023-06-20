import zmq
from ivy.std_api import *
import sys
from abstract_protocol import AbstractProtocol
from zeromq import ZeroMQProtocol
from ivy_protocol import IvyProtocol
from kafka_protocol import KafkaProtocol
from message_receiver import MessageReceiver

from time import sleep




def main_receive(protocol, message_count, port, length, queue, logger):
    
    com = "sub"
    if protocol == 'ivy':
        protocol_obj = IvyProtocol(port, logger)
        protocol_obj.initialize()
    elif protocol == 'zeromq':
        port = int(port)
        #port +=1
        protocol_obj = ZeroMQProtocol(port, com,logger)
        protocol_obj.initialize()
    elif protocol == 'kafka':
        protocol_obj = KafkaProtocol(com,logger)
        protocol_obj.initialize()
    else:
        print("Unsupported protocol: "+str(protocol))
        return

    logger.info('Démarrage du receveur')


    #envoie de message aà l'autre process pour signaler que le receveur est prêt
    queue.put("RECEIVER_READY")

    receiver = MessageReceiver(protocol_obj, protocol,length)
    receiver.receive_messages(message_count, queue)
    
    '''sender = MessageSender(protocol_obj)
    sender.send_messages(message_count)'''

