from django.contrib import admin

# Register your models here.
from .models import staticStockInfo, userInfo, userTransaction


class staticStockInfoAdmin(admin.ModelAdmin):
    # ...
    list_display = ('stock_name', 'exchange_name', 'ticker_name', 's_type')

class userInfoAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name')


admin.site.register(staticStockInfo, staticStockInfoAdmin)
admin.site.register(userInfo, userInfoAdmin)
admin.site.register(userTransaction)