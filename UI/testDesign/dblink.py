#!/usr/bin/env python

"""
Python module to connect the A-eye project to the mongodb database.
"""


import pymongo
import time
from bson.json_util import dumps
import json
client = pymongo.MongoClient("mongodb://localhost:27017/") #create mongodb client
db = client["dblink"]

def init():
    col = db["counter"]
    dict =[ {
        "_id": "personId",
        "seq": 0
    },
    {
        "_id": "logId",
        "seq": 0
    }]
    x=col.insert_many(dict)


def getNextSequence(collection,name):  
   return collection.find_and_modify(
       query= { '_id': name },
       update= { '$inc': {'seq': 1}},
       new=True
   ).get('seq');


def insert_person(name,
                  faceFile,
                  visits=0,
                  recentLog=-1
                 ):
    col = db["person"]
    id = getNextSequence(db.counter,"personId")  
    dict = { "_id": id,
             "personName": name, 
             "personFaceFile": faceFile,
             "personVisits": visits, 
             "personRecentLog": recentLog 
           }
    col.insert_one(dict)

def update_person(id,column,val):
    col = db["person"]
    query = { "_id": id}
    value = { "$set": { column: val} }
    col.update_one(query, value)

def insert_log(cam,personId,timestamp=0):
    if(timestamp == 0): # Add timestamp if no timestamp provided in the input
        timestamp=time.time()
    col = db["log"]
    id = getNextSequence(db.counter,"logId") 
    dict = { "_id": id,
            "logTimeStamp": timestamp,
            "logCam": cam,
            "personId": personId
           }
    #update the person collection
    update_person(personId,"personRecentLog",id)
    col.insert_one(dict)
def search_person(keyword,limit=5):
    col= db["person"]
    result = col.find({
        "personName" :{
            "$regex": keyword,
            '$options': 'i'
        }})
    return dumps(result) #return the object as a json string
if __name__ == "__main__":
    #To be run on terminal
    print(json.loads(search_person("a"))[0]['personName'])
