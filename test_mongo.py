from pymongo import MongoClient

uri = "mongodb://admin:admin123@localhost:27017"

client = MongoClient(uri)

db = client["mini_blog"]


collection = db["posts"]

result = collection.insert_one({
    "title": "First Post",
    "content": "Hello MongoDB"
})

print(f"Id: {result.inserted_id}")

doc = collection.find_one({"title": "First Post"})

print(f"found: {doc}")
