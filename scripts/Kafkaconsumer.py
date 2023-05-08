from kafka import KafkaConsumer
from json import loads
import time
import json
import requests
import pandas as pd
from threading import Timer
from datetime import datetime
from time import localtime, strftime
import os

mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())

#Instantiation du consumer
consumer = KafkaConsumer(
    "data",
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

print("ok2")

#Création d'un dataframe pour récupérer les données du consumer
dff = pd.DataFrame(columns =['Date', 'Station', 'Code Station','Etat de la station',
                                     'Nb bornes disponibles', 'Nombres de bornes en station', 'Nombre vélo en PARK+',
                                     'Nb vélo mécanique', 'Nb vélo électrique',
                                     'geo_lat','geo_long'])

#Pour chaque message arrivant dans le consumer sous fichier json, on parcourt les champs du fichier puis 
#on transfère le contenu de ceux qui nous intéréssent dans notre dataframe
for message in consumer:
    print("starting")
    message = message.value

    for rec in message['records']:

            dff.loc[len(dff)] = [mytime,
                                 rec['fields']['name'],
                                 rec['fields']['stationcode'],
                                 rec['fields']['is_installed'],
                                 rec['fields']['numbikesavailable'],
                                 rec['fields']['numdocksavailable'],
                                 rec['fields']['capacity'],
                                 rec['fields']['mechanical'],
                                 rec['fields']['ebike'],
                                 rec['fields']['coordonnees_geo'][0],
                                 rec['fields']['coordonnees_geo'][1]]
                                 
#Une fois les informations récépurées on ouvre le fichier de stockoge puis l'enregistre    
    with open("vélib_batch_par30.csv", 'a') as f:
        dff.to_csv(f, header=True, index=False)
        print( " - Fin de la récupération, Nb de lignes récupérées: ")
        

   
