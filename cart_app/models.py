from django.db  import models
 
class Order(models.Model):
    user           = models.ForeignKey('users.User', on_delete = models.CASCADE)
    total_price    = models.DecimalField(max_digits = 12, decimal_places = 0)
    final_price    = models.DecimalField(max_digits = 12, decimal_places = 0)
    size           = models.CharField(max_length = 30)
    product_image  = models.URLField(max_length = 1000)
    quantity       = models.IntegerField(default = 1)
    order_status   = models.ForeignKey('OrderStatus', on_delete = models.SET_NULL, null = True)
    product_color  = models.ManyToManyField('product_app.ProductColor', through = 'Cart')

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length = 30)
    
    class Meta:
        db_table = 'order_status'

class Cart(models.Model):
    product_color = models.ForeignKey('product_app.ProductColor', on_delete = models.CASCADE)
    order         = models.ForeignKey('Order', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'carts'
