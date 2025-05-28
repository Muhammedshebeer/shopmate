from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Product)
admin.site.register(Titlepage)
admin.site.register(Subtitles)
admin.site.register(Categories)
@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')  # Show these columns in admin list view
    search_fields = ('Name',)

@admin.action(description='Clear all Orders and OrderItems')
def clear_all_orders(modeladmin, request, queryset):
    OrderItem.objects.all().delete()
    Order.objects.all().delete()

    modeladmin.message_user(request, "All orders and order items have been deleted.")

class OrderAdmin(admin.ModelAdmin):
    actions = [clear_all_orders]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(CartItem)