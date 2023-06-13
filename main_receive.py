import zmq
from ivy.std_api import *
import sys
from abstract_protocol import AbstractProtocol
from zeromq import ZeroMQProtocol
from ivy_protocol import IvyProtocol
from kafka_protocol import KafkaProtocol
from message_receiver import MessageReceiver

from time import sleep




def main_receive(protocol, message_count, test_type, port, queue, logger):
    
    com = "sub"
    if protocol == 'ivy':
        args = sys.argv[4:]
        print(args)
        protocol_obj = IvyProtocol(port, logger)
        protocol_obj.initialize()
    elif protocol == 'zeromq':
        port = sys.argv[4]
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

    receiver = MessageReceiver(protocol_obj, protocol)
    receiver.receive_messages(message_count, test_type, queue)
    
    '''sender = MessageSender(protocol_obj)
    sender.send_messages(message_count)'''

