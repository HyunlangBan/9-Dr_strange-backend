from django.urls    import path
from cart_app.views import OrderView

urlpatterns = [
    path('', OrderView.as_view())
]
