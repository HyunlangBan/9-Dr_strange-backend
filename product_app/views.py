from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from .models import ProductColor, Product, Review
from users.models import UserProductColor
from django.db.models import Avg

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
