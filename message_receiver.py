from time import sleep, time
import time
import matplotlib.pyplot as plt
from statistics import mean


class MessageReceiver:
    def __init__(self, protocol_obj, bus, length):
        self.protocol_obj = protocol_obj
        self.bus = bus
        self.plt_data = []
        self.data=[]
        self.length = length
    
    
    def draw_graph(self, protocole, message_count):
        
        plt.plot(range(1, message_count+1), self.plt_data, 'ro')
        plt.xlabel('Message number')
        plt.ylabel('Time (s)')
        plt.title("temps moyens d'émission de "+str(message_count)+" messages de "+str(self.length)+" caractères avec "+str(protocole))
        print("La moyenne est", mean(self.plt_data))
        chemin_dossier = "graphiques"
        nom_fichier = 'graph '+str(self.bus)+' '+str(message_count)+'msgs de '+str(self.length)+' carac.png'
        chemin_complet = chemin_dossier + "/" + nom_fichier
        plt.savefig(chemin_complet)  # Enregistre le graphique dans un fichier
        plt.close()  # Ferme la figure pour libérer les ressources

        
    def receive_messages(self, message_count, test_type, queue):
        
        
            print("hey")
            self.data = self.protocol_obj.receive_message(message_count,queue)
            print(self.data)
            start_time = float(self.data[0][1].split("=")[1])
            
                    

            print(len(self.plt_data))
            for i in range(message_count):
                
                if self.data : 
                    t0 = float(self.data[i][1].split("=")[1]) 
                    time_interval = self.data[i][2] - t0
                    self.plt_data.append(time_interval)
            print("Temps total de communication : ", (self.data[-1][2] - start_time))

            self.draw_graph(self.bus, message_count) 
