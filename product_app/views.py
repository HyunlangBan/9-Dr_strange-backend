import json

from django.views import View
from django.http  import JsonResponse

from product_app.models import *

class ProductListView(View):
    def post(self, request, menu_name):
        product_list = ProductColor.objects.filter(product__sub_category__category__menu__name=menu_name).distinct()
        products = []
        for i in product_list:
            product = {}
            product['subCategoryId'] = i.product.sub_category.distinct()[0].id
            product['productNum'] = i.product_number
            product['productName'] = i.product.name
            product['like'] = 0
            product['color'] = i.color.name
            product['originPrice'] = i.product.price
            product['salePrice'] = i.discount_price
            images = i.productimage_set.all()
            image = []
            for s in images:
                image.append(s.image_url)
            product['productImg'] = image
            products.append(product)
        return JsonResponse({'products' : products})