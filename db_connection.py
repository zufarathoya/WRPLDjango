import pymongo

url = 'mongodb+srv://zufarathoyabahar:9y8lY9hiH5GY4YCW@wrpl.qkwukhm.mongodb.net/'
client = pymongo.MongoClient(url)

db = client['Gudang']
db_user = client['User']
