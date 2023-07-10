
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





def main_send(protocol, message_count, port,length, queue, logger, traitement, flag, flag_count, nbr_processes,direct_msg):




    com = "PUB"
    if protocol == 'ivy':
        args = port
        print(args)
        protocol_obj = IvyProtocol(args,logger,com)
        protocol_obj.initialize()

    elif protocol == 'zeromq':
        port = int(port) 
        #port+=1       
        protocol_obj = ZeroMQProtocol(port, com,logger)
        protocol_obj.initialize()
    elif protocol == 'kafka':
        protocol_obj = KafkaProtocol(com,logger)
        protocol_obj.initialize()
        
    else:
        print("Protocole invalide spécifié")
        return
    
    logger.info('Démarrage du sender')
    

    recvrdy=""
    while(not (str(nbr_processes-1) in recvrdy) ):
            #print(recvrdy)
            recvrdy = queue.get()
            #print(recvrdy)

    if True:
        sleep(2)


        length_of_string = int(length)
        message_rand=""
        if(flag):
            for j in range(flag_count):
                message_rand = message_rand+"flag"+str(j)+"="+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+" "

            message_rand = message_rand+"#"
        else:
            message_rand = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+"#"


        if protocol == "ivy":
            if direct_msg:
                for i in range(message_count):
                    start_time = time.time()
                    message = str(message_rand) + str(start_time)
                    #message = "hello =" + str(start_time)
                    #print(message)
                    protocol_obj.send_direct_message(message)
                    sleep(traitement)
        for i in range(message_count):
            start_time = time.time()
            message = str(message_rand) + str(start_time)
            #message = "hello =" + str(start_time)
            #print(message)
            protocol_obj.send_message(message)
            sleep(traitement)

        
        for i in range(1000):
            queue.put("LAST_MESSAGE")
        if protocol == "ivy":
            protocol_obj.stopsocket()