from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views
urlpatterns = [
    path('account', views.account, name='account'),
]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)