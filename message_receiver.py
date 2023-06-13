from time import sleep, time
import time
import matplotlib.pyplot as plt
from statistics import mean


class MessageReceiver:
    def __init__(self, protocol_obj, bus):
        self.protocol_obj = protocol_obj
        self.bus = bus
        self.plt_data = []
        self.data=[]
    
    
    def draw_graph(self, protocole, message_count):
        
        plt.plot(range(1, message_count+1), self.plt_data, 'ro')
        plt.xlabel('Message number')
        plt.ylabel('Time (s)')
        plt.title("temps moyens d'émission de "+str(message_count)+" messages courts avec "+str(protocole)+".")
        print("La moyenne est", mean(self.plt_data))
        plt.savefig('graph '+str(self.bus)+' '+str(message_count)+'msgs.png')  # Enregistre le graphique dans un fichier
        plt.close()  # Ferme la figure pour libérer les ressources

        
    def receive_messages(self, message_count, test_type, queue):
        
        
        if test_type == "total":
            print("hey")
            self.data = self.protocol_obj.receive_message(message_count,queue)
            print(self.data)
            start_time = float(self.data[1][1].split("=")[1])
            
                    
            print("Temps total de communication : ", (self.data[-1][2] - start_time))

         
        elif test_type == "graph":
            self.data = self.protocol_obj.receive_message(message_count,queue) 
            print(self.data)
            for i in range(message_count):
                
                if self.data : 
                    t0 = float(self.data[i][1].split("=")[1]) 
                    time_interval = self.data[i][2] - t0
                    self.plt_data.append(time_interval)

            self.draw_graph(self.bus, message_count)    
        else :
            print("mauvais type de test choisi. veuillez entrer soit graph soit total.")