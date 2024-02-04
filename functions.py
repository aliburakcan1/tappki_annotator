
import os
from pymongo.mongo_client import MongoClient
import time
import requests
from constant import fxtwitter_headers

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
    tweet_status = record["tweet_id"]
    try:
        fxtwitter_response = requests.get(f"https://api.fxtwitter.com/i/status/{tweet_status}", headers=fxtwitter_headers, verify=False)
        json_response = fxtwitter_response.json()
        tweet_download_link = json_response["tweet"]["media"]["videos"][0]["url"]
        tweet_timestamp = json_response["tweet"]["created_timestamp"]
        tweet_views = json_response["tweet"]["views"]
        tweet_sensitive = json_response["tweet"]["possibly_sensitive"]
        tweet_media_duration = json_response["tweet"]["media"]["videos"][0]["duration"]

        get_collection(username, password, database, db_name, "tweet").insert_one(
            {"id": tweet_status, 
                "timestamp": tweet_timestamp, 
                "download_link": tweet_download_link, 
                "views": tweet_views, 
                "sensitive": tweet_sensitive, 
                "media_duration": tweet_media_duration, 
                "inserted_at": int(time.time()),
                "source": "single_tweet",
                "is_deleted": False
                }
                )
    except:
        pass
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