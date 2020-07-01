from django.urls import path

from product_app.views import ProductDetailView

urlpatterns = [
    path('/<int:p_num>', ProductDetailView.as_view())
]
