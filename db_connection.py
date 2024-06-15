import pymongo

url = 'mongodb+srv://zufarathoyabahar:9y8lY9hiH5GY4YCW@wrpl.qkwukhm.mongodb.net/'
# url = 'mongodb://zufarathoyabahar:9y8lY9hiH5GY4YCW@wrpl.qkwukhm.mongodb.net/'

client = pymongo.MongoClient(url)

db = client['Gudang']
db_user = client['User']
db_pelanggan = client['Pelanggan']
db_buyers = client['dbBuyers']
db_bank = client['dbBank']
db_sales = client['dbSales']
db_supplier = client['dbSupplier']
db_delivery = client['dbDelivery']