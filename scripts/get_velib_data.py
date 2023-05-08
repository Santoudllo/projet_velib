import time
import json
import requests
from threading import Timer
from datetime import datetime
from time import localtime, strftime
import os

#fonction permettant de recupérer un nombre de lignes prédéfinie via l'API et de les afficher si elles sont disponibles
def get_velib_data():
    nrows=2
    print("starting")
    url= "https://data.opendatasoft.com/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel%40parisdata&q=&rows="+str(nrows)+""
    mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    resp = requests.get(url)
    
    if resp.status_code != 200:
        print(mytime, " - ",  " - Erreur dans la récupération des données")
    else:
        data = resp.json()
        print(data)
        
#Condition permettant de lancer le script 
if __name__== "__main__":
    get_velib_data()
  
