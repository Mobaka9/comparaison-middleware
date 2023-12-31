
from abc import ABC, abstractmethod
import random
import string
import time
from ingescape_protocol import IngescapeProtocol
from ivy.std_api import *
import sys
import getopt
from ivy_direct import IvyDirectProtocol
from ivy_protocol import IvyProtocol
from zeromq import ZeroMQProtocol
#from kafka_protocol import KafkaProtocol
from time import sleep





def main_send(protocol, message_count, port,length, queue, logger, traitement, flag, flag_count, nbr_processes, direct_msg, device):




    com = "PUB"
    if protocol == 'ivy':
        args = port
        if direct_msg:
            protocol_obj = IvyDirectProtocol(args,logger,com)
            protocol_obj.initialize()
        else:
            protocol_obj = IvyProtocol(args,logger,com,queue)
            protocol_obj.initialize()

    elif protocol == 'zeromq':
        port = int(port) 
        #port+=1       
        protocol_obj = ZeroMQProtocol(port, com,logger)
        protocol_obj.initialize()
    # elif protocol == 'kafka':
    #     protocol_obj = KafkaProtocol(com,logger)
    #     protocol_obj.initialize()
    elif protocol == 'ingescape':
        protocol_obj = IngescapeProtocol(com, port, device, None, queue)
        protocol_obj.initialize()
        
    else:
        print("Protocole invalide spécifié")
        return
    
    logger.info('Démarrage du sender')
    

    recvrdy=""
    count = 0
    while(count < (nbr_processes) ):
        recvrdy = queue.get()
        if "RECEIVER_READY" in recvrdy :                       
            print(str("j'ai recu ")+recvrdy )
            count +=1
            print(f"count {count}")
    print("we passed")
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


        for i in range(message_count):
            start_time = time.time()
            message = str(message_rand) + str(start_time)
            #message = "hello =" + str(start_time)
            #print(message)
            protocol_obj.send_message(message)
            #print(f"sending message n:{i}")
            sleep(traitement)

        results=[]
        print("envoi termine")
        #sleep(60)
        #protocol_obj.stopsocket()
        for i in range(1000):
            queue.put("LAST_MESSAGE")

        count_close=0
        recv_fin=""
        while( count_close < nbr_processes ):
            recv_fin = queue.get()
            if "close_sock" in recv_fin:
                print(recv_fin)
                count_close+=1
        while( len(results) < nbr_processes ):    
            recv_fin = queue.get()
            if "total" in recv_fin:

                results.append(float(recv_fin.split("#")[1]))
        print(results)
        #sleep(1)
        protocol_obj.stopsocket()