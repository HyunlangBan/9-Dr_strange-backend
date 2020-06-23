from django.db import models

class Sizes(models.Model):
    name = models.IntegerField(default = 0, unique = True)

    class Meta:
        db_table = 'sizes'


class ProductSizes(models.Model):
    products_w_colors = models.ManyToManyField('ProductsWColors', on_delete = models.CASCADE)
    sizes = models.ForeignKey('Sizes', on_delete = models.CASCADE) 

    class Meta:
        db_table = 'product_sizes'


class Materials(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = 'materials'

class Countries(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = 'countries'


