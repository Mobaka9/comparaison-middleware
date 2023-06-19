
from abc import ABC, abstractmethod
import random
import string
import time
from ivy.std_api import *
import sys
import getopt
from ivy_protocol import IvyProtocol
from zeromq import ZeroMQProtocol
from kafka_protocol import KafkaProtocol
from time import sleep





def main_send(protocol, message_count, port,length, queue, logger, traitement):




    com = "PUB"
    if protocol == 'ivy':
        args = port
        print(args)
        protocol_obj = IvyProtocol(args,logger)
        protocol_obj.initialize()

    elif protocol == 'zeromq':
        port = sys.argv[4]
        
        protocol_obj = ZeroMQProtocol(port, com,logger)
        protocol_obj.initialize()
    elif protocol == 'kafka':
        protocol_obj = KafkaProtocol(com,logger)
        protocol_obj.initialize()
        
    else:
        print("Protocole invalide spécifié")
        return
    
    logger.info('Démarrage du sender')
    

    message = queue.get()
    if message == "RECEIVER_READY":
        sleep(2)

        #calcul des résulat
        length_of_string = int(length)
        message_rand = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+"="

        #if test_type == "total":



    #elif test_type == "graph":
        for i in range(message_count):
            #print(i)

            start_time = time.time()
            message = str(message_rand) + str(start_time)
            #message = "hello =" + str(start_time)
            protocol_obj.send_message(message)
            sleep(traitement)
        #message = "last message =" + str(start_time)
        #protocol_obj.send_message(message, "10002")

            
        #else :

    
        for i in range(100):
            queue.put("LAST_MESSAGE")