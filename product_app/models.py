from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menus'
    
class MenuCategory(models.Model):
    menu     = models.ForeignKey('Menu', on_delete = models.SET_NULL, null = True)
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = 'menus_categories'

class Category(models.Model):
    name = models.CharField(max_length = 100)
    menu = models.ManyToManyField('Menu', through = 'MenuCategory')
    
    def __str__(self):
        return f'name: {self.name}, menus: {menu}'
    
    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name        = models.CharField(max_length = 100)
    category    = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return f'name: {self.name}, categories: {self.category}'

    class Meta:
        db_table = 'sub_categories'

class SubCategoryProduct(models.Model):
    subcategory = models.ForeignKey('SubCategory', on_delete = models.SET_NULL, null = True)
    product     = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'sub_category_products'

class Size(models.Model):
    name            = models.CharField(max_length=20, default = 0, unique = True)
    product_color   = models.ManyToManyField('ProductColor', through = 'ProductColorSize')

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
    price          = models.DecimalField(max_digits = 12, decimal_places = 0)
    material       = models.ForeignKey('Material', on_delete = models.SET_NULL, null = True)
    country        = models.ForeignKey('Country', on_delete = models.SET_NULL, null = True)
    sub_category   = models.ManyToManyField('SubCategory', through = 'SubCategoryProduct')
    
    def __str__(self):
        return f'name: {self.name}, price: {self.price}'
    
    class Meta:
        db_table = 'products'

class Color(models.Model):
    name     = models.CharField(max_length = 100, unique = True)
    product  = models.ManyToManyField('Product', through = 'ProductColor')

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    color            = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)
    product          = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
    product_number   = models.IntegerField(unique = True)
    user             = models.ManyToManyField('users.User', through='Review')
    detail_thumbnail = models.URLField(max_length = 2000)
    discount_price   = models.DecimalField(max_digits = 12, decimal_places = 0, null = True, blank = True)

    class Meta:
        db_table = 'product_colors'

class ProductColorSize(models.Model):
    product_color    = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True)
    size             = models.ForeignKey(Size, on_delete = models.SET_NULL, null = True)
    soldout          = models.BooleanField(default = False)

    class Meta:
        db_table = 'product_sizes'

class DetailImage(models.Model):
    image_url       = models.URLField(max_length = 2000)
    product_color   = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True)
    
    def __self__(self):
        return self.image_url

    class Meta:
        db_table = 'detail_images'

class ProductImage(models.Model):
    image_url     = models.URLField(max_length = 2000)
    product_color = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = 'product_images'

class Review(models.Model):
    user          = models.ForeignKey('users.User', on_delete = models.CASCADE)
    product_color = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True)
    title         = models.CharField(max_length=100)
    content       = models.CharField(max_length=1000)
    image_url     = models.URLField(max_length=1000)
    stars         = models.IntegerField()
    order         = models.OneToOneField('cart_app.Order', on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = 'reviews'
