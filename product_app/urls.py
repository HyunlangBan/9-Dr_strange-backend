from django.urls import path

from product_app.views import (
    ProductListView,
    ProductDetailView,
    SearchView
)

urlpatterns = [
    path('/list', ProductListView.as_view()),
    path('/<int:p_num>', ProductDetailView.as_view()),
    path('/search', SearchView.as_view())
]
