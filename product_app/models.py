from django.db import models

class Menus(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menus'
    

class Categories(models.Model):
    name  = models.CharField(max_length = 100)
    menus = models.ForeignKey(Menus, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, menus: {menus}'
    class Meta:
        db_table = 'categories'


class SubCategories(models.Model):
    name       = models.CharField(max_length = 100)
    categories = models.ForeignKey(Categories, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, categories: {self.categories}'
    class Meta:
        db_table = 'subcategories'


class Sizes(models.Model):
    name = models.IntegerField(default = 0, unique = True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sizes'


class Materials(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'materials'


class Countries(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = 'countries'


class Products(models.Model):
    name           = models.CharField(max_length                = 200, unique     = True)
    price          = models.IntegerField()
    materials      = models.ForeignKey(Materials, on_delete     = models.CASCADE)
    countries      = models.ForeignKey(Countries, on_delete     = models.CASCADE)
    sub_categories = models.ForeignKey(SubCategories, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'name: {self.name}, price: {self.price}'
    
    class Meta:
        db_table = 'products'


class Colors(models.Model):
    name     = models.CharField(max_length              = 100, unique        = True)
    products = models.ManyToManyField(Products, through = 'ProductsWColors')

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name


class ProductsWColors(models.Model):
    colors         = models.ForeignKey(Colors, on_delete   = models.CASCADE)
    products       = models.ForeignKey(Products, on_delete = models.CASCADE)
    like           = models.IntegerField(default           = 0)
    product_number = models.IntegerField(unique            = True)

    class Meta:
        db_table = 'productswcolors'
        
        
class ProductSizes(models.Model):
    products_w_colors = models.ManyToManyField(ProductsWColors)
    sizes             = models.ForeignKey(Sizes, on_delete = models.CASCADE)

    class Meta:
        db_table = 'product_sizes'


class Images(models.Model):
    image_url           = models.CharField(max_length = 1000)
    products_w_colors = models.ForeignKey(ProductsWColors, on_delete = models.CASCADE)
    
    def __self__(self):
        return self.image_url

    class Meta:
        db_table = 'images'



