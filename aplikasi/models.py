from django.db import models
from db_connection import db, db_user, db_pelanggan, db_buyers, db_bank, db_sales, db_supplier, db_delivery
from django.contrib.auth.models import User

product_collection = db['products']
user_collection = db_user['User']
cart_collection = db_buyers['Chart']
history_purchase = db_buyers['historyPurchase']
TopUpHistory = db_bank['TopUpHistory']
BankAccount = db_bank['BankAccount']
purchase = db_pelanggan['purchase']
history_request = db_sales['historyRequest']
sales_request = db_sales['request']
supplier_product = db_supplier['product']
sales_product = db_sales['product']
sales_history = db_sales['historySales']
delivery_req = db_delivery['delivery_request']

# class Product(models.Model):
#     nama = models.CharField(max_length=100)
#     harga = models.DecimalField(max_digits=10, decimal_places=2)
#     stok = models.IntegerField()
#     kategori = models.CharField(max_length=50)

#     def __str__(self):
#         return self.nama

# class BankAccount(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bank_name = models.CharField(max_length=255)
#     account_number = models.CharField(max_length=50)
#     account_holder_name = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.bank_name} - {self.account_holder_name}"

# class TopUpHistory(models.Model):
#     TRANSACTION_TYPES = (
#         ('P', 'Payment'),
#         ('R', 'Refund'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
#     transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     order_id = models.CharField(max_length=255, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"TopUpHistory {self.order_id} - {self.user.username}"