from typing import Union
from fastapi import FastAPI
import pymongo
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
client = pymongo.MongoClient()
db = client['main']
collection = db["meals"]

class Meals(BaseModel):
        main: str
        sides: Union[str, None] = None
        date: Union[str, None] = None
        auth: str

class Range(BaseModel):
        beginning: str
        end: str

@app.get("/")
def read_root():
        return {"resp": 200}

@app.post("/add")
def read_item(f: Meals):
        if f.auth != os.environ.get("CLIENT_PASS"):
                return {"resp": 403}
        else:
                print(dict((y, x) for x, y in f))
                db.collection.insert_one(dict((x, y) for x, y in f))
                return {"resp": 200}

@app.post("/load")
def read_from_db(f: Range):
        result = db.collection.aggregate([
        {
                '$match': {
                'date': {
                        '$gt': f.beginning,
                        '$gt': f.end
                }
                }
        }
        ])
        print(f.beginning)
        appended_list = []
        for i in result:
                appended_list.append(i)
        print(appended_list)
        return{"resp": str(appended_list)}
