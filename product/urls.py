from django.conf.urls import url

from product.views import index, subcategory_product, product_details, cart, remove_product_from_session


app_name = 'product'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<id>\d+)/$', subcategory_product,
        name='subcategory-product'),
    url(r'^(?P<id>\d+)/details/$', product_details,
        name='product-details'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^remove-product/$', remove_product_from_session, name='remove-product'),
]