
import os
from pymongo.mongo_client import MongoClient

def split_lines(folder_name):
    for filename in os.listdir(os.path.join("data", folder_name)):
        with open(os.path.join("data", folder_name, filename), encoding="utf8") as f:
            lines = f.read().splitlines()
            for line in lines:
                yield line

def get_collection(username, password, database, db_name, collection_name):

    uri = f"mongodb+srv://{username}:{password}@{database}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)

    db = client[db_name]
    collection = db[collection_name]

    return collection

def write_to_db(username, password, database, db_name, collection_name, record):
    get_collection(username, password, database, db_name, collection_name).insert_one(record)


def find_all_ids(username, password, database):

    uri = f"mongodb+srv://{username}:{password}@{database}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)
    
    db = client.tepki
    annotation = db.video

    ids = annotation.find({}, {"tweet_id": 1, "_id": 0})

    return [id["tweet_id"] for id in ids]

def find_record_by_id(username, password, database, db_name, collection_name, tweet_id):

    record = get_collection(username, password, database, db_name, collection_name).find_one({"tweet_id": tweet_id})
    return record

def is_exist(username, password, database, db_name, collection_name, tweet_id):
    record = get_collection(username, password, database, db_name, collection_name).find_one({"tweet_id": tweet_id})
    return True if record else False