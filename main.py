import argparse
import logging
import os
import platform
import subprocess
import sys
import multiprocessing
from main_send import main_send
from main_receive import main_receive
from time import sleep


def start_zookeeper():
    subprocess.run(['zookeeper-server-start', '/usr/local/etc/kafka/zookeeper.properties'])


def start_kafka():
    subprocess.run(['kafka-server-start', '/usr/local/etc/kafka/server.properties'])



def main():
    

    


    parser = argparse.ArgumentParser(description='Envoi de messages entre 2 terminaux avec 3 middleware', add_help=True)
    parser.add_argument('--protocol', help='Protocole à utiliser (ivy, zeromq, kafka)')
    parser.add_argument('--message_count', default = 1, type=int, help='Nombre de messages à envoyer')
    parser.add_argument('--port', help='Port ou addresse (seulement pour ivy)')
    parser.add_argument('--length',default='3000', help='longueur du message à envoyer (3000 carac par défaut)')
    parser.add_argument('--log_level', default='FATAL', help='Niveau de configuration de la journalisation')
    parser.add_argument('--sleep',default='0',type = float, help="Temps du sleep à mettre entre l'envoi de chaque message")
    parser.add_argument('--flag', action='store_true', help="activer les flags pour simuler l'utilisation de regexp")
    parser.add_argument('--flag_count', default = 1, type=int, help='Nombre de flags à envoyer')
    parser.add_argument('--nbr_receivers', default = 1, type=int, help='Nombre de receveurs créés')
    parser.add_argument('--direct_msg', action='store_true', help="envoyer des messages ivy avec ivydirectmsg")
    parser.add_argument('--device', default=None,help='nom du peripherique réseau utilisé pour ingescape')

#n

    param = parser.parse_args()


    # Configurer la journalisation
    logging.basicConfig(
        level=param.log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log',mode='w')
        ]
    )

    logger = logging.getLogger(__name__)
    multi_recv = False
    if param.nbr_receivers != 1:
        multi_recv = True
    if param.protocol == "kafka":
        my_os = platform.system()

        if my_os == "Darwin":
            
            kafka_processes = [
                multiprocessing.Process(target=start_zookeeper),
                multiprocessing.Process(target=start_kafka)
            ]
            for process in kafka_processes:
                process.start()
                sleep(3)
            sleep(6)

        elif my_os == "Linux":
            os.system("systemctl start zookeeper")
            os.system("systemctl start kafka")            
            

    queue = multiprocessing.Queue()
    logger.info('Démarrage du programme')
    nmbre_rec= param.nbr_receivers
    recv_processes=[]
    for i in range(nmbre_rec):
        receive_process = multiprocessing.Process(target=main_receive, args=(param.protocol, param.message_count, param.port,param.length, queue, logger, param.flag, i,param.nbr_receivers, multi_recv,param.direct_msg, param.device))
        recv_processes.append(receive_process)
    send_process = multiprocessing.Process(target=main_send, args=(param.protocol, param.message_count, param.port, param.length, queue, logger, param.sleep, param.flag, param.flag_count, param.nbr_receivers, param.direct_msg, param.device))
    for i in range(nmbre_rec):
        recv_processes[i].start()
    #sleep(2)
    send_process.start()
    '''
    receive_process2 = multiprocessing.Process(target=main_receive, args=(param.protocol, param.message_count, 3000,param.length, queue, logger))
    send_process2 = multiprocessing.Process(target=main_send, args=(param.protocol, param.message_count, 3000, param.length, queue, logger, param.sleep))
    
    receive_process2.start()
    send_process2.start()
'''
    results=[]
    recv_fin=""
    # while(len(results) != param.nbr_receivers ):
    #         recv_fin = queue.get()
    #         if "total" in recv_fin:
    #             results.append(float(recv_fin.split("#")[1]))
    #         print(f"Temps total de tous les processeurs{max(results)}")
    send_process.join()
    receive_process.join()

#    send_process2.join()
#   receive_process2.join()

    send_process.kill()
    receive_process.kill()
    
    if param.protocol == "kafka":
        if my_os == "Darwin":
            logger.info('Arrêt des services Kafka')
            for process in kafka_processes:
                process.kill()

    logger.info('Fin du programme')
if __name__ == '__main__':
    main()
