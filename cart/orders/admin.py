from django.contrib import admin
from .models import Order, OrderedItem


class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'owner',
        'order_status',
        'delete_status',
        'created_at',
    )

    list_filter = (
        'order_status',
        'delete_status',
    )

    inlines = [OrderedItemInline]


@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'product',
        'quantity',
        'owner',
    )