from django.views import View
from django.http  import JsonResponse

from product_app.models import ProductColor

class BestSellerView(View):
    def get(self, request):
        product_list = ProductColor.objects.prefetch_related(
                'product__menu_category_sub_category__menu_category__menu'
                ).prefetch_related(
                'productcolorsize_set__size')
        
        # 일부 상품
        product_smooth = ProductColor.objects.select_related('product').get(product_number = 10072600)
        product_myles  = ProductColor.objects.select_related('product').get(product_number = 23523001)
        product_ryker  = ProductColor.objects.select_related('product').get(product_number = 24515001)
        
        # 일부 상품 제외한 전체 상품
        products_women = product_list.filter(
                product__menu_category_sub_category__menu_category__menu__name = 'women').distinct()
        products_men   = product_list.filter(
                product__menu_category_sub_category__menu_category__menu__name = 'men').distinct()
        all_items      = product_list.all()

        DEFAULT_LIKES  = 600
       
        smooth = [
            {
                'productName'   : product_smooth.product.name,
                'like'          : 370,
                'color'         : product_smooth.color.name,
                'productImg'    : [img.image_url for img in product_smooth.productimage_set.all()],
                'size'          : {"220" : False, "230" : False, "240" : False, "250" : False,
                                   "260" : False, "270" : True, "280" : True, "290" : False},
                'originPrice'   : product_smooth.product.price,
                'salePrice'     : product_smooth.discount_price,
                'productNum'    : product_smooth.product_number,
                'subCategoryId' : product_smooth.product.menu_category_sub_category.first().sub_category.id
            }
        ]

        myles = [
            {
                'productName'   : product_myles.product.name,
                'like'          : 1611,
                'color'         : product_myles.color.name,
                'productImg'    : [img.image_url for img in product_myles.productimage_set.all()],
                'size'          : {"220" : False, "230" : False, "240" : False, "250" : True,
                                   "260" : False, "270" : True, "280" : True, "290" : False},
                'originPrice'   : product_myles.product.price,
                'salePrice'     : product_myles.discount_price,
                'productNum'    : product_myles.product_number,
                'subCategoryId' : product_myles.product.menu_category_sub_category.first().sub_category.id
            }
        ]

        ryker = [
            {
                'productName'   : product_ryker.product.name,
                'like'          : 1611,
                'color'         : product_ryker.color.name,
                'productImg'    : [img.image_url for img in product_ryker.productimage_set.all()],
                'size'          : {"220" : True, "230" : True, "240" : True, "250" : False,
                                   "260" : False, "270" : False, "280" : True, "290" : False},
                'originPrice'   : product_ryker.product.price,
                'salePrice'     : product_ryker.discount_price,
                'productNum'    : product_ryker.product_number,
                'subCategoryId' : product_ryker.product.menu_category_sub_category.first().sub_category.id
            }
        ]

        product_women = [
            {
                'productName'   : item.product.name,
                'like'          : DEFAULT_LIKES + item.userproductcolor_set.count(), 
                'color'         : item.color.name,
                'productImg'    : [img.image_url for img in item.productimage_set.all()],
                'size'          : {"220" : True, "230" : False, "240" : False, "250" : True,
                                   "260" : False, "270" : True, "280" : False, "290" : False},
                'originPrice'   : item.product.price,
                'salePrice'     : item.discount_price,
                'productNum'    : item.product_number,
                'subCategoryId' : item.product.menu_category_sub_category.first().sub_category.id
            } for item in products_women if item.product_number not in (10072600, 23523001, 24515001)]
        
        product_men = [
            {
                'productName'   : item.product.name,
                'like'          : DEFAULT_LIKES + item.userproductcolor_set.count(), 
                'color'         : item.color.name,
                'productImg'    : [img.image_url for img in item.productimage_set.all()],
                'size'          : {"220" : True, "230" : False, "240" : False, "250" : True, 
                                   "260" : False, "270" : True, "280" : False, "290" : False},
                'originPrice'   : item.product.price,
                'salePrice'     : item.discount_price,
                'productNum'    : item.product_number,
                'subCategoryId' : item.product.menu_category_sub_category.first().sub_category.id
            } for item in products_men if item.product_number not in (10072600, 23523001, 24515001)]

        return JsonResponse({
            'productFirst' : smooth,
            'productSecond' : myles, 
            'productThird' : ryker,
            'women' : product_women,
            'men' : product_men
            }, status = 200)
