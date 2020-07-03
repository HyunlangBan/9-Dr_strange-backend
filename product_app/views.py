import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg

from product_app.models import (
    ProductColor,
    Product,
    Review
)
from users.models       import UserProductColor

class ProductListView(View):
    def get(self, request):
        data = json.loads(request.body)
        product_number = data['productNum']
        
        # product
        menu_name = request.GET.get('menu_name', None)
        product_list = ProductColor.objects.prefetch_related('product__menu_category_sub_category__menu_category__menu')
        gender_product = product_list.filter(product__menu_category_sub_category__menu_category__menu__name = menu_name).distinct()
        DEFAULT_LIKES = 600

        # sizes
        product_color_size_objects = ProductColor.objects.prefetch_related('productcolorsize_set').get(product_number = product_number)
        all_items = product_color_size_objects.productcolorsize_set.all()
        all_sizes = [ item.size.name for item in all_items ]
        in_stock_list = [ item.size.name for item in all_items.filter(soldout = False) ]
        size_soldout = dict()
        for size in all_sizes:
            if size not in in_stock_list:
               size_soldout[size] = True
            else:
                size_soldout[size] = False

        products = [
            {   
                'subCategoryId' : single_product.product.menu_category_sub_category.first().sub_category.id,
                'productNum'    : single_product.product_number,
                'size'          : size_soldout,
                'productName'   : single_product.product.name,
                'like'          : DEFAULT_LIKES+single_product.userproductcolor_set.count(),
                'color'         : single_product.color.name,
                'originPrice'   : single_product.product.price,
                'salePrice'     : single_product.discount_price,
                'productImg'    : [img.image_url for img in single_product.productimage_set.all()]
            } for single_product in gender_product ]
        return JsonResponse({'products' : products})

class ProductDetailView(View):
    def get(self, request, p_num):

        ## product_name
        related_product = ProductColor.objects.select_related('product').get(product_number = p_num)
        product_name = related_product.product.name
        
        ## sizes
        pcs = ProductColor.objects.prefetch_related('productcolorsize_set').get(product_number = p_num)
        all_items = pcs.productcolorsize_set.all()
        all_sizes = [ item.size.name for item in all_items ]
        in_stock = all_items.filter(soldout = False)
        in_stock_list = [ item.size.name for item in in_stock ]
        size_soldout = dict()
        for i in all_sizes:
            if i not in in_stock_list:
               size_soldout[i] = True
            else:
                size_soldout[i] = False
        
        # images
        detail_product = ProductColor.objects.prefetch_related('detailimage_set', 'product').get(product_number= p_num)
        all_images = detail_product.detailimage_set.all()
        images = [ image.image_url for image in all_images ]
        
        # thumbnails
        p_id = detail_product.product.id
        all_products = ProductColor.objects.filter(product_id = p_id)
        
        product_thumbnails = dict()
        for product in all_products:
            p_n = product.product_number
            p_t = product.detail_thumbnail
            product_thumbnails[p_n] = p_t
        
        # original, sale price
        original_price = detail_product.product.price
        sale_price = ProductColor.objects.get(product_number = p_num).discount_price
        
        # material, country
        prod = Product.objects.select_related('material', 'country').get(id = p_id)
        material = prod.material.name
        country = prod.country.name
        
        # review
        reviews = Review.objects.prefetch_related('product_color__order_set__user')
        review_all = reviews.filter(product_color__product_number=p_num)
        review_count = review_all.count()
        review_info = [
                {
                    'name': r.order.user.name,
                    'title': r.title,
                    'img': r.image_url,
                    'rating': r.stars,
                    'content': r.content,
                    'size': r.order.cart_set.first().size
                }
        for r in review_all ]
       
        # avg_rate
        avg = review_all.aggregate(average_rate=Avg('stars'))
        
        # like
        likes = UserProductColor.objects.select_related('product_color')
        all_like = likes.filter(product_color__product_number = p_num).count()

        fake_like = 600

        result = {
                "productName": product_name,
                "size": size_soldout,
                "productImg": images,
                "productThumbnail": product_thumbnails,
                "originPrice": original_price,
                "salePrice": sale_price,
                "material": material,
                "country": country,
                "reviewInfo": review_info,
                "averageRate": '%.1f' % avg['average_rate'],
                "reviewCount": review_count,
                "like": all_like + fake_like,
                }
        
        return JsonResponse({'productDetailInfo':result}, status=200)

class SearchView(View):
    def get(self, request):
        search_term = request.GET.get('search_term', None)
        DEFAULT_LIKES = 600
        if search_term:
            products = ProductColor.objects.select_related('product')
            search_result = products.filter(product__name__contains=search_term)

            products = [
            {
                'productNum'    : single_product.product_number,
                'productName'   : single_product.product.name,
                'like'          : DEFAULT_LIKES+single_product.userproductcolor_set.count(),
                'color'         : single_product.color.name,
                'originPrice'   : single_product.product.price,
                'salePrice'     : single_product.discount_price,
                'productImg'    : [img.image_url for img in single_product.productimage_set.all()]
            } for single_product in search_result]
            return JsonResponse({'products' : products}, status = 200)
        else:
            return JsonResponse({'message': "No results."}, status = 200)