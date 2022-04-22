from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['title', 'saler', 'client', 'signed']
    list_filter = ['saler', 'client', 'signed']
    fieldsets = (
        ("Contract informations",
         {'fields': ('title', 'amount', 'payment_due', 'client')}),
        ("Support informations",
         {'fields': ('saler', 'signed')}),
        ("Date informations",
         {'fields': ('date_created', 'date_updated')}),
    )
    readonly_fields = ('client', 'date_created', 'date_updated')
    search_fields = ['title']
    ordering = ['saler']
