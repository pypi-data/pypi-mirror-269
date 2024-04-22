from pymongo import MongoClient

class MongoDBClient:
    def __init__(self,connection_string):
        self.client = MongoClient(connection_string)
        self.domain = self.client.domain
