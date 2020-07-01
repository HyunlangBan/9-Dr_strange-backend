from django.db import models

class User(models.Model):
    name         = models.CharField(max_length = 100)
    nickname     = models.CharField(max_length = 100)
    password     = models.CharField(max_length = 300)
    birthday     = models.DateField()
    email        = models.EmailField(max_length = 100, unique = True)
    phone_number = models.CharField(max_length = 30)

    class Meta:
        db_table = 'users'

class UserProductColor(models.Model):
    is_like       = models.BooleanField(default = True)
    user          = models.ForeignKey('User', on_delete = models.CASCADE)
    product_color = models.ForeignKey('product_app.ProductColor', on_delete = models.CASCADE)

    class Meta:
        db_table = 'users_product_colors'