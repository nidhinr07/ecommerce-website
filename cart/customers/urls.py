from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views
urlpatterns = [
    path('account', views.account, name='account'),
    path('logout',views.sign_out, name='logout'),
]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)