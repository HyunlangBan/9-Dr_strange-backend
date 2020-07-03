from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('products', include('product_app.urls')),
    path('cart', include('cart_app.urls')),
    path('bestseller', include('bestseller_app.urls'))
]
