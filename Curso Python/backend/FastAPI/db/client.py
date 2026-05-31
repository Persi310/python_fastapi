from pymongo import MongoClient
from pymongo.server_api import ServerApi

#OPjLTG7PvB4lYXUR
uri = "mongodb+srv://admin:OPjLTG7PvB4lYXUR@cluster0.36fx70y.mongodb.net/?appName=Cluster0"

db_client = MongoClient(uri, server_api=ServerApi('1')).Cluster0
try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
#db_client = MongoClient().local

