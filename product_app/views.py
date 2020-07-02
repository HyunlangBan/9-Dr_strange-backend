import json

from django.views import View
from django.http  import JsonResponse

from product_app.models import ProductColor

class ProductListView(View):
    def get(self, request):
        menu_name = request.GET.get('menu_name', None)
        product_list = ProductColor.objects.prefetch_related('product__menu_category_sub_category__menu_category__menu')
        gender_product = product_list.filter(product__menu_category_sub_category__menu_category__menu__name = menu_name).distinct()
        DEFAULT_LIKES = 600
        products = [
            {
                'subCategoryId' : single_product.product.menu_category_sub_category.first().sub_category.id,
                'productNum'    : single_product.product_number,
                'productName'   : single_product.product.name,
                'like'          : DEFAULT_LIKES+single_product.userproductcolor_set.count(),
                'color'         : single_product.color.name,
                'originPrice'   : single_product.product.price,
                'salePrice'     : single_product.discount_price,
                'productImg'    : [img.image_url for img in single_product.productimage_set.all()]
            } for single_product in gender_product ]
        return JsonResponse({'products' : products})