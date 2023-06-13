import zmq
import getopt
import os
import string
from abc import ABC, abstractmethod
from ivy.std_api import *
from time import sleep, time
import sys
from kafka import KafkaProducer
import time


class AbstractProtocol(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_message(self, message):
        pass


class IvyProtocol(AbstractProtocol):
    def initialize(self, ivybus):
        IVYAPPNAME = 'pyhello'
        sisreadymsg = '[%s is ready]' % IVYAPPNAME
        
        def oncxproc(agent, connected):
            if connected == IvyApplicationDisconnected:
                print('Ivy application %r was disconnected' % agent)
            else:
                print('Ivy application %r was connected' % agent)
            print('Current Ivy applications are [%s]' % IvyGetApplicationList())

        def ondieproc(agent, _id):
            print('Received the order to die from %r with id = %d' % (agent, _id))

        IvyInit(IVYAPPNAME, sisreadymsg, 0, oncxproc, ondieproc)
        IvyStart(ivybus)

    def send_message(self, message):
        IvySendMsg(message)


class ZeroMQProtocol(AbstractProtocol):
    def __init__(self, port):
        self.port = port
        self.socket = None

    def initialize(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDHWM, 2000000)
        self.socket.bind("tcp://*:%s" % self.port)

    def send_message(self, message):
        self.socket.send_string(message)


class KafkaProtocol(AbstractProtocol):
    def __init__(self):
        self.kafka_producer = None

    def initialize(self):
        self.kafka_producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))

    def send_message(self, topic_name, message):
        try:
            string_bytes = str.encode(message)
            self.kafka_producer.send(topic_name, value=string_bytes)
            self.kafka_producer.flush()
        except Exception as ex:
            print(str(ex))


class MessageSender:
    def __init__(self, protocol):
        self.protocol = protocol

    def send_messages(self, message_count):
        self.protocol.initialize()
        sleep(2)

        for i in range(message_count):
            start_time = time.time()
            message = "hello =" + str(start_time)
            self.protocol.send_message(message)


def main():
    if len(sys.argv) < 4:
        print("Pas assez d'arguments: python3 send.py [protocol] [message_count] [port ou adresse broadcast(ivy)]")
        return

    protocol = sys.argv[1]
    message_count = int(sys.argv[2])

    if protocol == 'ivy':
        ivybus = sys.argv[3]
        protocol_obj = IvyProtocol()
        protocol_obj.initialize(ivybus)
    elif protocol == 'zeromq':
        port = sys.argv[3]
        protocol_obj = ZeroMQProtocol(port)
        protocol_obj.initialize()
    elif protocol == 'kafka':
        protocol_obj = KafkaProtocol()
        protocol_obj.initialize()
    else:
        print("Protocole invalide spécifié")
        return

    sender = MessageSender(protocol_obj)
    sender.send_messages(message_count)


if __name__ == '__main__':
    main()