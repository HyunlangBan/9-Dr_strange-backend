from django.urls import path

from bestseller_app.views import BestSellerView

urlpatterns = [
    path('', BestSellerView.as_view())
]
