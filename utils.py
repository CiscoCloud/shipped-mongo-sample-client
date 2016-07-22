from pymongo import MongoClient, errors
from bson import ObjectId
import os


MONGODB_URI = "mongodb://mongodb:27017/mongo"

SEED_DATA = [{'counter':0}]
id = ""
client = None

def dbConnection():
    deployTarget = os.environ.get('DEPLOY_TARGET')
    constr = os.environ.get('HOST_MONGODB_SINGLE')
    for i in range(0, 10):
        if i > 0:
            print("DB connection attempt %d of 10 failed; retrying (%s) connect string (%s)", i)

        # ex: "mongodb://mongodb:27017/mongo?sslmode=disable"
        if deployTarget == "LOCAL_SANDBOX":
            constr = MONGODB_URI


        print("Current deploy target %s" % deployTarget)
        #print(connstr)
        try:
            client = MongoClient(constr)
            db = client.get_default_database()#['example-db']
            return db
        except errors.ServerSelectionTimeoutError as err:
            print(err, constr)


def setupDB():
    db = dbConnection()

    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
    else:
        tbl_counter = db['tbl_counter']
        id = tbl_counter.insert(SEED_DATA)
        return id



def closeDB():
    client.close()