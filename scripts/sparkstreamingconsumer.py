import os
#packages nécessaires à l'intégration de spark et kafka
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 pyspark-shell'
import findspark
import json
#permet de trouve le répertoire de spark 
findspark.init('/opt/spark')
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,LongType,IntegerType,StringType,ArrayType,DoubleType
from pyspark.sql.functions import split, explode,window,from_json,col,current_timestamp,avg
from pyspark.sql.functions import from_json
from variables import bootstrap_servers,kafka_topic
checkpoint_path = "./checkpoint/te"


#ouvre le fichier qui contient le schéma json ( la structure des données à récupérer)
f = open("./schema.json")
json_file = json.load(f)
#Transforme le schéma sous forme de StructType , format qu'utile pyspark 
schemaFromJson = StructType.fromJson(json_file)


#Création d'une instance SparkSession(le point d'entrée de toutes les fonctionnalités de Spark)
spark = (SparkSession
        .builder
        .appName("consumer_structured_streaming")  
        .getOrCreate())



#la fonctionalité readStream de SparkSession est utilisée pour charger les données à partir de Kafka.
data_stream= spark \
            .readStream \
            .format("kafka").option("kafka.bootstrap.servers", bootstrap_servers) \
            .option("subscribe",kafka_topic).option("failOnDataLoss","false").option("startingOffsets", "latest").load()\
            .selectExpr("CAST(value AS STRING) as value")           



# Organisation des données en dataframe 
df= data_stream.select(from_json(col("value"), schemaFromJson).alias("data"))\
.select("data.*")\
.select(explode(col("data.stations")).alias("info"))\
.select(col("info.*"),explode(col("info.num_bikes_available_types")).alias("type"))\
.select("*","type.*").drop("type","num_bikes_available_types")\
.withColumn("eventime", current_timestamp())                    



#Calcul des moyennes des colonnes 
averages =df.withWatermark("eventime", "3 minutes").groupBy("stationCode",window("eventime","2 minutes")).agg(avg("num_bikes_available").alias("Avg_numbikesavailable"), 
         avg("ebike").alias("Avg_ebike"),
         avg("mechanical").alias("Avg_mechanical_bikes")
        )


#affiche la structure des données
df.printSchema()


#Affiche le dataframe 
query = averages.writeStream.format("console")\
        .outputMode("complete")\
        .option("checkpointLocation", checkpoint_path) \
        .start()\
         .awaitTermination()                                      
