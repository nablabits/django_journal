from django.contrib import admin
from .models import Income, Hour, Customer

admin.site.register(Hour)
admin.site.register(Customer)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'who', 'cash', 'tip', 'comments')
    list_filter = ('who', )
