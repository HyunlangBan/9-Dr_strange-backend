from django.db  import models
 
class Order(models.Model):
    user           = models.ForeignKey('users.User', on_delete = models.CASCADE)
    total_price    = models.DecimalField(max_digits = 12, decimal_places = 0)
    final_price    = models.DecimalField(max_digits = 12, decimal_places = 0)
    product_color  = models.ManyToManyField('product_app.ProductColor', through = 'Cart')
    
    def __str__(self):
        return f'total: {self.total_price}, discount: {self.discount_price}, final: {self.final_price}'

    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    product_color = models.ForeignKey('product_app.ProductColor', on_delete = models.CASCADE)
    order         = models.ForeignKey('Order', on_delete = models.SET_NULL, null = True)
    quantity      = models.IntegerField()

    def __str__(self):
        return f'quantity: {self.quantity}'

    class Meta:
        db_table = 'carts'
