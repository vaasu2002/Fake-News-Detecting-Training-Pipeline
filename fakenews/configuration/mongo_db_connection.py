import certifi
import os
import pymongo

from fakenews.constant.database import DATABASE_NAME
MONGODB_URL_KEY = "mongodb+srv://vaasubisht2021:gFS7waCLecumTpV7@cluster0.qcixkpq.mongodb.net/test"
ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY # os.getenv(MONGODB_URL_KEY)
                print(mongo_db_url)
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

        except Exception as e:
            raise 