from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bson

class Conexion:
    def __init__(self):
        load_dotenv()
        self.MONGO_URL=os.environ['MONGODB_URL3']
    def connectionDB(self):
        try:
            client = MongoClient(self.MONGO_URL)
            db=client["SO-Project-2024"]
        except ConnectionError:
            print("Error de Conexion con la base de datos")
        return db


#try:
    #load_dotenv()
    #client = MongoClient(os.environ["MONGODB_URL2"])
    #database =client["SO-Project-2024"]
    #database["Usuario"].insert_one({"Nombre": "IAN","Numero":789})
    #print("todo bien")
#except ConnectionError:
    #print("Error de Conexion con la base de datos")
