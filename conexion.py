from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bson

class Conexion:
    def __init__(self):
        load_dotenv()
        self.MONGO_URL=os.environ['MONGODB_URL2']
    def connectionDB(self):
        try:
            client = MongoClient(self.MONGO_URL)
            db=client["SO-Project-2024"]
        except ConnectionError:
            print("Error de Conexion con la base de datos")
        return db
