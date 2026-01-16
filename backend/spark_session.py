# backend/spark_session.py
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Taxi_Project") \
    .master("local[*]") \
    .getOrCreate()
