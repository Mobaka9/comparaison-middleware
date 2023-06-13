import subprocess
from time import sleep


def start_kafka_services():
    # Démarrer ZooKeeper
    subprocess.run(['zookeeper-server-start', '/usr/local/etc/kafka/zookeeper.properties'])
    sleep(3)
    # Démarrer Kafka
    subprocess.run(['kafka-server-start', '/usr/local/etc/kafka/server.properties'])

if __name__ == '__main__':
    start_kafka_services()