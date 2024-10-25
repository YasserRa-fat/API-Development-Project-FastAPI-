from fastapi import FastAPI
from pymongo import MongoClient
import redis

app = FastAPI()

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['your_database']
collection = db['your_collection']

# Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/data")
def get_data():
    data = collection.find_one({"name": "example"})
    if data:
        return {"data": data}
    else:
        return {"message": "No data found"}

@app.post("/cache")
def cache_data(key: str, value: str):
    redis_client.set(key, value)
    return {"message": f"Cached {key}: {value}"}

@app.get("/cache/{key}")
def get_cached_data(key: str):
    value = redis_client.get(key)
    if value:
        return {"value": value.decode('utf-8')}
    else:
        return {"message": f"No cache found for key {key}"}
