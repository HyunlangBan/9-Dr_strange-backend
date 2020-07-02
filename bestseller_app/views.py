from django.views import View
from django.http  import JsonResponse

from product_app.models import *

class BestSellerView(View):
    def get(self, request):
        product_list = ProductColor.objects.prefetch_related('product__subcategoryproduct_set__subcategory__category__menucategory_set__menu')
        for item in product_list:
            product_name = item.product.name
            product_number = item.product_number
            sub_category_id = item.product.sub_category.all()[0].id
            menu_name = item.product.sub_category.all()[0].category.menu.all()[0].name
            like = like
            color = color
            original_price = original_price
            sale_price = sale_price
