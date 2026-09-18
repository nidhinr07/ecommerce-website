from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views
urlpatterns = [
    path('cart', views.my_cart, name='cart'),
]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)