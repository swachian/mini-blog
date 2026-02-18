from pymongo import MongoClient

uri = "mongodb://admin:admin123@localhost:27017"

client = MongoClient(uri)

db = client["mini_blog"]

posts_collection = db["posts"]
