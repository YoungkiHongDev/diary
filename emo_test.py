import pymongo

client = pymongo.MongoClient("mongodb+srv://DiaryAdmin:<password>@cluster0.znsdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

print(db)