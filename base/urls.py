from django.conf.urls import url, include
from django.contrib import admin
from product.views import checkout


urlpatterns = [
    url(r'', include('product.urls')),
    url(r'^admin/', admin.site.urls),
]
