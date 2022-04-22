from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'email',
        'company_name', 'sales_contact']
    list_filter = ['company_name', 'sales_contact']
    fieldsets = (
        ('Client informations', {
            'fields': ('first_name', 'last_name', 'company_name')}),
        ('Client contact', {
            'fields': ('email', 'phone', 'mobil')}),
        ('Sale contact', {
            'fields': ('sales_contact',)}),
        ("Date informations", {
            'fields': ('date_created', 'date_updated')}),
    )
    readonly_fields = ('date_created', 'date_updated')
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
