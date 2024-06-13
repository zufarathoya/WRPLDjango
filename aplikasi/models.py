from django.db import models
from db_connection import db, db_user, db_pelanggan, dbBuyers
# Create your models here.


product_collection = db['products']
user_collection = db_user['User']
cart_collection = dbBuyers['Chart']
history_purchase = dbBuyers['historyPurchase']

# class Product(models.Model):
#     nama = models.CharField(max_length=100)
#     harga = models.DecimalField(max_digits=10, decimal_places=2)
#     stok = models.IntegerField()
#     kategori = models.CharField(max_length=50)

#     def __str__(self):
#         return self.nama