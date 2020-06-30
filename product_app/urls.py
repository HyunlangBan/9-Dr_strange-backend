from django.urls import path

from product_app.views import ProductListView

urlpatterns = [
    path('/list/<str:menu_name>', ProductListView.as_view())
]