from flask import Flask, render_template
from bson import ObjectId
from utils import *

import json

app = Flask(__name__)
id = []

@app.route("/")
def hello():
    id = setupDB()
    db = dbConnection()
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
    cursor = tbl_counter.find()
    result = {}
    for entry in cursor:
        result = entry
        i = result['counter']
        return render_template("index.html", count=i)

@app.route("/count",  methods=['GET'])
def getData():
    db = dbConnection()
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')
        cursor = tbl_counter.find()
        result={}
        for entry in cursor:
            result=entry
            i = result['counter']
            return render_template("index.html", count = i)


@app.route("/like",  methods=['POST'])
def postData():
    db = dbConnection()
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')

        tbl_counter.update(tbl_counter.find_one(), {'$inc': {'counter':1}},  upsert=False)
        result = (tbl_counter.find_one())
        return render_template("index.html", count = result['counter'])

@app.route("/reset",  methods=['POST'])
def resetData():
    db = dbConnection()
    if "tbl_counter" in db.collection_names():
        tbl_counter = db.get_collection('tbl_counter')

        tbl_counter.update(tbl_counter.find_one(), {'$set': {'counter': 0}}, upsert=False)
        result = (tbl_counter.find_one())
        return render_template("index.html", count = result['counter'])


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')




