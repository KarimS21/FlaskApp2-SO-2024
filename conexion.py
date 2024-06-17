from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bson

class Conexion:
    def __init__(self):
        load_dotenv()
        self.MONGO_URL=os.environ['MONGODB_URL'] #cambiar al 2 para que funcione con la base de datos de riva en su docker 
    def connectionDB(self):
        try:
            client = MongoClient(self.MONGO_URL)
            db=client["Project-So-2024"]
        except ConnectionError:
            print("Error de Conexion con la base de datos")
        return db

