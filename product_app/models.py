from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menus'
    
class MenuCategory(models.Model):
    menu     = models.ForeignKey('Menu', on_delete = models.SET_NULL, null = True, related_name='menu_category')
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True, related_name='menu_category')
    
    class Meta:
        db_table = 'menus_categories'

class Category(models.Model):
    name = models.CharField(max_length = 100)
    menu = models.ManyToManyField('Menu', through = 'MenuCategory', related_name='category')
    
    def __str__(self):
        return f'name: {self.name}, menus: {menu}'
    
    class Meta:
        db_table = 'categories'

class CategorySubcategory(models.Model):
    category     = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True, related_name='category_subcategory')
    sub_category = models.ForeignKey('SubCategory', on_delete = models.SET_NULL, null = True, related_name='category_subcategory')

    class Meta:
        db_table = 'cateogries_subcategories'

class SubCategory(models.Model):
    name        = models.CharField(max_length = 100)
    description = models.CharField(max_length = 1000)
    category    = models.ManyToManyField('Category', through = 'CategorySubcategory', related_name='sub_category')
    
    def __str__(self):
        return f'name: {self.name}, categories: {self.category}'

    class Meta:
        db_table = 'sub_categories'

class Size(models.Model):
    name            = models.CharField(max_length=20, default = 0, unique = True)
    product_color   = models.ManyToManyField('ProductColor', through = 'ProductColorSize', related_name='size')

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
    material       = models.ForeignKey('Material', on_delete = models.SET_NULL, null = True, related_name='product')
    country        = models.ForeignKey('Country', on_delete = models.SET_NULL, null = True, related_name='product')
    sub_category   = models.ForeignKey('SubCategory', on_delete = models.SET_NULL, null = True, related_name='product')
    
    def __str__(self):
        return f'name: {self.name}, price: {self.price}'
    
    class Meta:
        db_table = 'products'

class Color(models.Model):
    name     = models.CharField(max_length = 100, unique = True)
    product  = models.ManyToManyField('Product', through = 'ProductColor', related_name='color')

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    color          = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True, related_name='product_color')
    product        = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, related_name='product_color')
    product_number = models.IntegerField(unique = True)
    user           = models.ManyToManyField('users.User', through='Review', related_name='product_color')

    class Meta:
        db_table = 'product_colors'

class ProductColorSize(models.Model):
    product_color    = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True, related_name='product_color_size')
    size             = models.ForeignKey(Size, on_delete = models.SET_NULL, null = True, related_name='product_color_size')
    soldout          = models.BooleanField(default = False)

    class Meta:
        db_table = 'product_sizes'

class DetailImage(models.Model):
    image_url       = models.CharField(max_length = 1000)
    product_color   = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True, related_name='detail_image')
    
    def __self__(self):
        return self.image_url

    class Meta:
        db_table = 'detail_images'

class ProductImage(models.Model):
    image_url     = models.CharField(max_length = 1000)
    product_color = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True, related_name='product_image')
    
    class Meta:
        db_table = 'product_images'

class ProductColorDetailThumbnail(models.Model):
    product_color    = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True, related_name='product_color_detail_thumbnail')
    detail_thumbnail = models.ForeignKey('DetailThumbnail', on_delete = models.SET_NULL, null = True, related_name='product_color_detail_thumbnail')

    class Meta:
        db_table = 'product_colors_detail_thumbnails'
        
class DetailThumbnail(models.Model):
    image_url = models.CharField(max_length=1000)

    class Meta:
        db_table = 'detail_thumbnails'

class Reveiw(models.Model):
    user          = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name='review')
    product_color = models.ForeignKey('ProductColor', on_delete = models.SET_NULL, null = True, related_name='review')
    title         = models.CharField(max_length=100)
    content       = models.CharField(max_length=1000)
    image_url     = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'reviews'
