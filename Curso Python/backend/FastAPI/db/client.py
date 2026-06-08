from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import Settings

db_client = MongoClient(Settings.URI, server_api=ServerApi('1')).Cluster0
try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
#db_client = MongoClient().local

