from abc import ABC, abstractmethod


class AbstractProtocol(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_message(self, message, topic):
        pass

    @abstractmethod
    def receive_message(self):
        pass 