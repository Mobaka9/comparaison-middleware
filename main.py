import argparse
import logging
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
    parser.add_argument('--message_count', type=int, help='Nombre de messages à envoyer')
    parser.add_argument('--port', help='Port ou addresse (seulement pour ivy)')
    parser.add_argument('--length',default='3000', help='longueur du message à envoyer (3000 carac par défaut)')
    parser.add_argument('--log_level', default='INFO', help='Niveau de configuration de la journalisation')
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
    
    if param.protocol == "kafka":
        kafka_processes = [
            multiprocessing.Process(target=start_zookeeper),
            multiprocessing.Process(target=start_kafka)
        ]
        for process in kafka_processes:
            process.start()
            sleep(3)
        sleep(6)


    queue = multiprocessing.Queue()
    logger.info('Démarrage du programme')

    receive_process = multiprocessing.Process(target=main_receive, args=(param.protocol, param.message_count, param.port,param.length, queue, logger))
    send_process = multiprocessing.Process(target=main_send, args=(param.protocol, param.message_count, param.port, param.length, queue, logger))
    receive_process.start()
    #sleep(2)
    send_process.start()


    send_process.join()
    receive_process.join()

    send_process.kill()
    receive_process.kill()
    
    if param.protocol == "kafka":
        logger.info('Arrêt des services Kafka')
        for process in kafka_processes:
            process.kill()

    logger.info('Fin du programme')
if __name__ == '__main__':
    main()
