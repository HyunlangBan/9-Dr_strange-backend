from django.db import models

class Menus(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'menus'
    
class Categories(models.Model):
    name = models.CharField(max_length=100)
    menus = models.ForeignKey(Menus, on_delete=models.CASCADE)
    class Meta:
        db_table = 'categories'

class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'subcategories'


# class images(models.Model):
#     img_url = models.CharField(max_length=1000)
#     products_w_colors = models.ForeignKey(ProductsWColors, on_delete=models.CASCADE)
#     class Meta:
#        db_table = 'images'