from pymongo import MongoClient, errors
from bson import ObjectId
import os

#default URI for local bootstap from CLI
MONGODB_URI = "mongodb://mongodb:27017@admin:mongo/mongo"
#intial data that needs to be seeded
SEED_DATA = [{'counter':0}]
id = ""
client = None

def dbConnection():
	#gets environment variable "DEPLOY_TARGET" value 
    deployTarget = os.environ.get('DEPLOY_TARGET')
	#gets environment variable "HOST_RABBITMQ" value
    constr = os.environ.get('HOST_MONGODB_SINGLE')
	#Retries to connect to Db for 10 times before throwing an error
    for i in range(0, 10):
        if i > 0:
            print("DB connection attempt %d of 10 failed; retrying (%s) connect string (%s)", i)

        # ex: "mongodb://mongodb:27017@admin:mongo/mongo?sslmode=disable"
		#checks whether it is a local bootstrap or being deployed some centralized server
        if deployTarget == "LOCAL_SANDBOX":
            constr = MONGODB_URI

        try:
			#creates alient with embedded mongo db
            client = MongoClient(constr)
            db = client.get_default_database()#['example-db']
            return db
        except errors.ServerSelectionTimeoutError as err:
            print(err, constr)


def setupDB():
    db = dbConnection()
	#checks if table exists or not before creating one
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
    else:
        tbl_counter = db['tbl_counter']
        id = tbl_counter.insert(SEED_DATA)
        return id



def closeDB():
    client.close()