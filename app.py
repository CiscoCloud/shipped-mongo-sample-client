from flask import Flask, render_template
from bson import ObjectId
from utils import *

import json

app = Flask(__name__)
id = []

# returns the UI
@app.route("/")
def hello():
	#getting a mongodb connection
    db = dbConnection()
	#get an existing table
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
		#get no of likes
        result = (tbl_counter.find_one())
    return render_template("index.html", count=result['counter'])

#posts the count of likes
@app.route("/like",  methods=['POST'])
def postData():
	#getting a mongodb connection
    db = dbConnection()
	#get an existing table
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
		#update vale of likes to current no. of like + 1
        tbl_counter.update(tbl_counter.find_one(), {'$inc': {'counter':1}},  upsert=False)
		#get no of likes
        result = (tbl_counter.find_one())
        return str(result['counter'])

#resets like to 0
@app.route("/reset",  methods=['POST'])
def resetData():
	#getting a mongodb connection
    db = dbConnection()
	#get an existing table
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
		#update vale of likes to 0
        tbl_counter.update(tbl_counter.find_one(), {'$set': {'counter': 0}}, upsert=False)
		#get no of likes
        result = (tbl_counter.find_one())
        return str(result['counter'])


if __name__ == "__main__":
    setupDB()
    app.run(debug=True,host='0.0.0.0')




