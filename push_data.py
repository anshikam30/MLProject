from dotenv import load_dotenv
import os
import json 
import sys


load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi #Make secure http connections
ca = certifi.where()


import pandas as pd
import numpy as np
import pymongo
from  src.exception import NetworkSecurityException
from src.logger import logging


class NetworkDataExtract():
    def __init__(self):
        
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self, file_path):
        
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace = True)
            records = list(json.loads(df.T.to_json()).values()) #Every record is a json entry
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def insert_data_to_mongo(self,records,database,collection):
        
        try:
            self.database = database
            self.collection = collection
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "/Users/anshikamodi/Anshika/KrishNaik/Mlops/MLProject/Network_Data/phisingData.csv"
    DATABASE = "ANSHIKAAI"
    COLLECTION = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_convertor(FILE_PATH)
    num_records = network_obj.insert_data_to_mongo(records, DATABASE, COLLECTION)
    print(f"Number of Records in Data is {num_records}.")