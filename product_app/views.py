from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from .models import *
from users.models import *

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
        detail_images = ProductColor.objects.prefetch_related('detailimage_set').get(product_number= p_num)
        all_images = detail_images.detailimage_set.all()
        images = [ image.image_url for image in all_images ]
        
        # thumbnails
        related_products = ProductColor.objects.prefetch_related('product').get(product_number = p_num)
        p_id = related_products.product.id
        all_products = ProductColor.objects.filter(product_id = p_id)
        
        product_thumbnails = dict()
        for product in all_products:
            p_n = product.product_number
            p_t = product.detail_thumbnail
            product_thumbnails[p_n] = p_t
        
        # original, sale price
        original_price = related_products.product.price
        sale_price = ProductColor.objects.get(product_number = p_num).discount_price
        
        # material
        p_material = Product.objects.select_related('material').get(id = p_id)
        material = p_material.material.name
        
        # country
        p_country = Product.objects.select_related('country').get(id = p_id)
        country = p_country.country.name
        
        # review
        reviews = Review.objects.prefetch_related('product_color__order_set__user')
        review_all = reviews.filter(product_color__product_number=p_num)
        review_count = review_all.count()
        star_list = []
        review_info = []
        for r in review_all:
            review_dict = {}
            review_dict['name'] = r.order.user.name
            review_dict['title'] = r.title
            review_dict['img'] = r.image_url
            review_dict['rating'] = r.stars
            star_list.append(r.stars)
            review_dict['content'] =r.content
            review_dict['size'] = r.order.cart_set.first().size
            review_info.append(review_dict)
       
        # avg_rate
        try:
            average_rate = sum(star_list)/(review_count*1.0)
            
        except ZeroDivisionError:
            average_rate = 0
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
                "averageRate": '%.1f' % average_rate,
                "reviewCount": review_count,
                "like": all_like + fake_like,
                }
        
        return JsonResponse({'productDetailInfo':result}, status=200)

