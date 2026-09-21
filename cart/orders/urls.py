from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views
urlpatterns = [
    path('cart', views.my_cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('remove_item/<pk>', views.remove_item_from_cart, name="remove_item"),
    path('checkout_item/<pk>', views.checkout_item, name="checkout_item"),
    path('order-status', views.order_status, name='order_status'),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)