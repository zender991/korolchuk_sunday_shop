from django.contrib import admin

from product.models import (Category,
                            Subcategory,
                            Product,
                            Order)


class OrdersAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'subtotal']
    list_display = ('name', 'email', 'subtotal')


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Order, OrdersAdmin)