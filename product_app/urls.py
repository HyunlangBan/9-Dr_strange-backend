from django.urls import path

from product_app.views import ProductListView

urlpatterns = [
    path('/list', ProductListView.as_view())
]