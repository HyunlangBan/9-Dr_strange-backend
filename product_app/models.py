from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menus'
    
class MenuCategory(models.Model):
    menus      = models.ForeignKey(Menu, on_delete = models.CASCADE)
    categories = models.ForeignKey('Category', on_delete = models.CASCADE)

class Category(models.Model):
    name  = models.CharField(max_length = 100)
    menus = models.ManyToManyField(Menu, through = 'MenuCategory')
    
    def __str__(self):
        return f'name: {self.name}, menus: {menus}'
    class Meta:
        db_table = 'categories'

class CategorySubcategory(models.Model):
    categories     = models.ForeignKey(Category, on_delete = models.CASCADE)
    sub_categoreis = models.ForeignKey('SubCategory', on_delete = models.CASCADE)

class SubCategory(models.Model):
    name         = models.CharField(max_length = 100)
    descriptions = models.CharField(max_length = 1000)
    categories   = models.ManyToManyField(Category, through = 'CategorySubcategory')
    
    def __str__(self):
        return f'name: {self.name}, categories: {self.categories}'
    class Meta:
        db_table = 'sub_categories'


class Size(models.Model):
    name = models.CharField(max_length=20, default = 0, unique = True)
    
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
    products = models.ManyToManyField(Product, through = 'ProductColor')

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    colors         = models.ForeignKey(Color, on_delete = models.CASCADE)
    products       = models.ForeignKey(Product, on_delete = models.CASCADE)
    product_number = models.IntegerField(unique = True)
    # user           = models.ManyToManyField(User, through='Review')

    class Meta:
        db_table = 'products_colors'


class Reveiw(models.Model):
    # user            = models.ForeignKey(User, on_delete = models.CASCADE)
    products_colosr = models.ForeignKey(ProductColor, on_delete = models.CASCADE)
    title           = models.CharField(max_length=100)
    contents        = models.CharField(max_length=1000)
    image_url       = models.CharField(max_length=1000)


class ProductSize(models.Model):
    products_colors   = models.ManyToManyField(ProductColor)
    sizes             = models.ForeignKey(Size, on_delete = models.CASCADE)

    class Meta:
        db_table = 'product_sizes'


class Image(models.Model):
    image_url           = models.CharField(max_length = 1000)
    products_colors     = models.ForeignKey(ProductColor, on_delete = models.CASCADE)
    
    def __self__(self):
        return self.image_url

    class Meta:
        db_table = 'images'


class ListThumnail(models.Model):
    image_url       = models.CharField(max_length=1000)
    products_colors = models.ForeignKey(ProductColor, on_delete = models.CASCADE)


class ProductcolorProductthumnail(models.Model):
    products_colors   = models.ForeignKey(ProductColor, on_delete = models.CASCADE)
    product_thumnails = models.ForeignKey('ProductThumnail', on_delete = models.CASCADE)


class ProductThumnail(models.Model):
    image_url = models.CharField(max_length=1000)


class Review(models.Model):
    # user = models.ForeignKey(User, on_delete = models.CASCADE)
    products_colors = models.ForeignKey(ProductColor, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    contents = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000, null = True)
