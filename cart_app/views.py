import json

from django.views           import View
from django.http            import (
    JsonResponse,
    HttpResponse
)
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
    FieldDoesNotExist
)

from users.decorator        import login_check
from users.models           import (
    User,
    UserProductColor
)
from product_app.models     import (
    Size,
    Product,
    Color,
    ProductColor,
    ProductColorSize,
    DetailImage
)
from cart_app.models        import (
    Order,
    OrderStatus,
    Cart
)

class OrderView(View):
    PENDING = 1
    DEFAULT_LIKES = 600

    @login_check
    def post(self, request):
        try:
            user_id                = request.user.id
            data                   = json.loads(request.body)
            product                = ProductColor.objects.prefetch_related(
                                    'product__color_set'
                                    ).prefetch_related(
                                    'detailimage_set'
                                    ).get(product_number = product_number)
            product_color_id       = product.id
            product_id             = product.product.id
            color_name             = product.color.name
            product_image          = product.detailimage_set.first().image_url
            product_number         = data['productNum']
            total_price            = data['currentOrigin']
            total_sale_price       = data['currentSale']
            quantity               = data['currentQuantity']
            size                   = data['currentSize']
            total_discounted_price = total_price - total_sale_price
            final_price            = total_price - total_discounted_price
          
            if not Order.objects.filter(user_id = user_id, order_status_id = PENDING).exists(): 
                Order(
                    user_id         = user_id,
                    total_price     = total_price,
                    final_price     = final_price,
                    order_status_id = PENDING
                ).save()
                order_id = Order.objects.get(user_id = user_id, order_status_id = PENDING).id
            else:
                order              = Order.objects.get(user_id = user_id, order_status_id = PENDING)
                order.total_price  += total_price
                order.final_price  += final_price
                order.save()
                order_id           = order.id
                cart_items         = Cart.objects.filter(order_id = order_id)
            Cart(
                product_color_id = product_color_id,
                order_id         = order_id,
                size             = size,
                quantity         = quantity
            ).save()
            return HttpResponse(status = 200)
        
        except ObjectDoesNotExist:
            return HttpResponse(status = 400)
        except KeyError:
            return HttpResponse(status = 400)
        except TypeError:
            return HttpResponse(status = 400)
    
    @login_check
    def get(self, request):
        user_id = request.user.id
        try:
            order_id     = Order.objects.get(user_id = user_id, order_status_id = PENDING)
            cart_items   = Cart.objects.prefetch_related(
                          'order__product_color__product__color_set'
                          ).prefetch_related(
                          'order__user__userproductcolor_set'
                          ).filter(order_id = order_id) 
            product_list = [
                    {
                        "productName"       : item.product_color.product.name,
                        "productImg"        : item.product_color.detailimage_set.first().image_url,
                        "color"             : item.product_color.color.name,
                        "size"              : item.size,
                        "singleOriginPrice" : item.product_color.product.price * item.quantity,
                        "singleSalePrice"   : item.product_color.discount_price * item.quantity,
                        "quantity"          : item.quantity,
                        "like"              : DEFAULT_LIKES + item.order.user.userproductcolor_set.count()
                    }
            for item in cart_items]
            
            total_price            = 0
            total_discounted_price = 0
            final_price            = 0
            for item in cart_items:
                total_price            += item.order.total_price
                total_discounted_price += (item.order.final_price - item.order.total_price)
                final_price            += item.order.final_price
            return JsonResponse(
                {
                    "products"             : product_list,
                    "totalPrice"           : total_price,
                    "totalDiscountedPrice" : total_discounted_price,
                    "finalPrice"           : final_price
                }, status=200)
        
        except ObjectDoesNotExist:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)
        except FieldDoesNotExist:
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)
