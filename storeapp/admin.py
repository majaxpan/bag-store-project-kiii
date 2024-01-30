from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'complete', 'transaction_id')

    def order_id(self, obj):
        return str(obj.id)

    def customer_name(self, obj):
        return obj.customer.name if obj.customer else None


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('street_name', 'street_number', 'city', 'country', 'zipcode')


admin.site.register(ShippingAddress, ShippingAddressAdmin)