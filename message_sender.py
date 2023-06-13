import random
import string
from time import sleep, time
import time


class MessageSender:
    def __init__(self, protocol):
        self.protocol = protocol

    def send_messages(self, message_count, type):
        
        
        if type == "total":
            length_of_string = 100000
            message_rand = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+"="

            start_time = time.time() 
            for i in range(message_count):
                #print(i)


                message = str(message_rand) + str(start_time)     #utiliser pour generer une chaine aleatoire
                #message = "hello =" + str(start_time)              #utiliser pour envoyer un message hello court
                self.protocol.send_message(message)
            #message = "last message =" + str(start_time)
            #self.protocol.send_message(message, "10002")
        elif type == "graph":
            for i in range(message_count):
                #print(i)
                length_of_string = 3000

                message_rand = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+"="
                start_time = time.time()
                message = str(message_rand) + str(start_time)
                #message = "hello =" + str(start_time)
                self.protocol.send_message(message)
            #message = "last message =" + str(start_time)
            #self.protocol.send_message(message, "10002")
        else :
            print("mauvais type de test choisi. veuillez entrer soit graph soit total.")