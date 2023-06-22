from time import sleep, time
import time
import matplotlib.pyplot as plt
from statistics import mean


class MessageReceiver:
    def __init__(self, protocol_obj, bus, length, protocol):
        self.protocol_obj = protocol_obj
        self.bus = bus
        self.plt_data = []
        self.data=[]
        self.length = length
        self.protocol = protocol
    
    
    def draw_graph(self, protocole, message_count):
        
        plt.plot(range(1, message_count+1), self.plt_data, 'ro')
        plt.xlabel('Message number')
        plt.ylabel('Time (s)')
        title = "temps individuels d'émission de "+str(message_count)+" messages de "+str(self.length)+" caractères avec "+str(protocole)
        plt.title(title, loc='center', wrap=True)
        print("La moyenne est", mean(self.plt_data))
        chemin_dossier = "graphiques"
        nom_fichier = 'graph '+str(self.bus)+' '+str(message_count)+'msgs de '+str(self.length)+' carac.png'
        chemin_complet = chemin_dossier + "/" + nom_fichier
        plt.savefig(chemin_complet)  # Enregistre le graphique dans un fichier
        plt.close()  # Ferme la figure pour libérer les ressources

        
    def receive_messages(self, message_count, queue, flag):
        
        
            print("hey")
            self.data = self.protocol_obj.receive_message(message_count,queue)
            self.protocol_obj.stopsocket()
            print(self.data)

            if(flag):
                if self.protocol != "ivy":
                    for i in range(message_count):
                        start_time = float(self.data[0][1].split("#")[1])

                        if self.data : 
                            message, t0 = self.data[i][1].split("#")
                            t0= float(t0)
                            elements = message.split(" ")
                            elements.pop()
                            print(elements)
                            contenus = [element.split("=")[1].strip() for element in elements]
                            print(contenus)
                    print("Temps total de communication : ", (time.time() - start_time))
                else:
                    
                    print("Temps total de communication : ", (time.time() - float(self.data[0][-1])))

                    

            else: 
                start_time = float(self.data[0][1].split("#")[1])
                for i in range(message_count):
                    if self.data : 
                        t0 = float(self.data[i][1].split("#")[1]) 
                        time_interval = self.data[i][2] - t0
                        self.plt_data.append(time_interval)
                print("Temps total de communication : ", (self.data[-1][2] - start_time))

                self.draw_graph(self.bus, message_count) 
