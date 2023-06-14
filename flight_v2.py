import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir du fichier CSV
data = pd.read_csv("resources/CSV_006/logFlightParam20230130-1739-49.csv")

# Extraire les colonnes du temps et des données d'intérêt
time = data["timestamp"]
alt = data["alt"]
vz = data["vz"]
ground_speed = data["groundSpeed"]
air_speed = data["airSpeed"]
loc_dev = data["locDev"]
gs_dev = data["gsDev"]

#f_eng1 = data["FF_Eng1"]
#f_eng2 = data["FF_Eng2"]
fob = data["FOB"]

gd_speed = data["gdSpeed"]


# Créer une figure et des axes
fig, ax1 = plt.subplots()

ax1.set_xlabel("Temps")

# Tracer la première courbe avec son échelle
ax1.plot(time, loc_dev, label="Ground speed", color='blue')
ax1.set_ylabel("Ground speed", color='blue')

# Configurer l'échelle des valeurs de l'axe des ordonnées de la première courbe
ax1.tick_params(axis='y', labelcolor='blue')

# Créer un deuxième axe partageant le même axe des abscisses
ax2 = ax1.twinx()

# Tracer la deuxième courbe avec son échelle
ax2.plot(time, gd_speed, label="Gd speed", color='red')
ax2.set_ylabel("Gd speed", color='red')

# Configurer l'échelle des valeurs de l'axe des ordonnées de la deuxième courbe
ax2.tick_params(axis='y', labelcolor='red')

# Ajouter une légende
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2)

# Afficher le graphe
plt.show()