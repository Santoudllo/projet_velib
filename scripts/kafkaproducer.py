import os
import time
import threading
import json
import requests
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import KafkaError
from threading import Timer
from datetime import datetime
from time import localtime, strftime
import os
from variables import bootstrap_servers,streaming_url,kafka_topic

#fonction permettant de recuperer les données via l'API et de les envoyer dans le canal d'information (kafka_topic)
def getData():
    print("starting")
    url= streaming_url
    mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda value: json.dumps(value).encode('utf-8'))
    resp = requests.get(url)

    df = {"fields":[]}
    if resp.status_code != 200:
        print(mytime, " - ",  " - Erreur dans la récupération des données")
    else:
        msg= resp.json()
        
    
        
        print(msg)
         
        producer.send(kafka_topic, msg)
        producer.flush()
    
#fonction permettant de lancer la fonction getData toutes les minutes   
def main():
    starttime = time.time()
    while True:
        getData()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        
#Condition permettant de lancer le script    
if __name__== "__main__":
    main()
