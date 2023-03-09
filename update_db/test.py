import json
import pymongo
import codecs
import boto3
import pandas as pd

DATABASE_URI = os.getenv("DATABASE_URI")
BUCKET_NAME = os.getenv("BUCKET_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


s3 = boto3.client('s3')
client = pymongo.MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


bucket_name = 'BUCKET_NAME'
# file_name = "2023_03_07_2021_09_13_dfrac.json"
    
def lambda_handler(event, context):
    
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)

    df = pd.read_json(obj['Body'])
    list_of_dict = df.to_dict(orient='records')
    collection.insert_many(list_of_dict)
    
    return {
        'statusCode': 200,
        'body': 'MongoDB Database updated'
    }
