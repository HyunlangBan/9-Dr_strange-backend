from django.db import models
from product_app.models import ProductColor

class User(models.Model):
    name         = models.CharField(max_length = 100)
    nickname     = models.CharField(max_length = 100)
    password     = models.CharField(max_length = 300)
    birthday     = models.DateField()
    email        = models.EmailField(max_length = 100, unique = True)
    phone_number = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'

class UserProductColor(models.Model):
    like          = models.IntegerField()
    user          = models.ForeignKey('User', on_delete = models.CASCADE)
    product_color = models.ForeignKey('ProductColor', on_delete = models.CASCADE)

    def __str__(self):
        return self.like

    class Meta:
        db_table = 'users_product_colors'