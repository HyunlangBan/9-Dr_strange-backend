from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menus'
    

class Category(models.Model):
    name  = models.CharField(max_length = 100)
    menus = models.ForeignKey(Menu, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, menus: {menus}'
    class Meta:
        db_table = 'categories'


class SubCategory(models.Model):
    name       = models.CharField(max_length = 100)
    categories = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, categories: {self.categories}'
    class Meta:
        db_table = 'sub_categories'


class Size(models.Model):
    name = models.IntegerField(default = 0, unique = True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sizes'


class Material(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'materials'


class Country(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = 'countries'


class Product(models.Model):
    name           = models.CharField(max_length = 200, unique = True)
    price          = models.IntegerField()
    materials      = models.ForeignKey(Material, on_delete = models.CASCADE)
    countries      = models.ForeignKey(Country, on_delete = models.CASCADE)
    sub_categories = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, price: {self.price}'
    
    class Meta:
        db_table = 'products'


class Color(models.Model):
    name     = models.CharField(max_length = 100, unique = True)
    products = models.ManyToManyField(Product, through = 'ProductWColor')

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name


class ProductWColor(models.Model):
    colors         = models.ForeignKey(Color, on_delete = models.CASCADE)
    products       = models.ForeignKey(Product, on_delete = models.CASCADE)
    like           = models.IntegerField(default = 0)
    product_number = models.IntegerField(unique = True)

    class Meta:
        db_table = 'productswcolors'
        
        
class ProductSize(models.Model):
    products_w_colors = models.ManyToManyField(ProductWColor)
    sizes             = models.ForeignKey(Size, on_delete = models.CASCADE)

    class Meta:
        db_table = 'product_sizes'


class Image(models.Model):
    image_url           = models.CharField(max_length = 1000)
    products_w_colors = models.ForeignKey(ProductWColor, on_delete = models.CASCADE)
    
    def __self__(self):
        return self.image_url

    class Meta:
        db_table = 'images'
