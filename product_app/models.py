from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    # materials = models.ForeignKey(Materials, on_delete = models.CASCADE)
    # countries = models.ForeignKey(Countires, on_delete = models.CASCADE)
    # sub_categories = models.ForeignKey(Countries, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, price: {self.price}'
    
    class Meta:
        db_table = 'products'

class Colors(models.Model):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Products, through='ProductsWColors')

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name

class ProductsWColors(models.Model):
    colors = models.ForeignKey(Colors, on_delete = models.CASCADE)
    products = models.ForeignKey(Products, on_delete = models.CASCADE)
    like = models.IntegerField(default=0)
    product_number = models.IntegerField(unique=True)

    class Meta:
        db_table = 'productswcolors'
