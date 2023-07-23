from bson import ObjectId
from pymongo import MongoClient
import pydantic

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


client = MongoClient("mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority")
db = client["core_data"]

coll_club_activity_history = db["club_activity_history"]