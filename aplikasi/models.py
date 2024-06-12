from django.db import models
from db_connection import db, db_user
# Create your models here.


produuct_collection = db['products']
user_collection = db_user['User']