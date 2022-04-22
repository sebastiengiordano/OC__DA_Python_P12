from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['contract', 'client', 'technician', 'status']
    list_filter = ['technician', 'status']
    fieldsets = (
        ("Event informations", {
            'fields': ('status', 'attendees', 'event_date', 'note')}),
        ("Support informations", {
            'fields': ('technician',)}),
        ("Client informations", {
            'fields': ('client', 'contract')}),
        ("Date informations", {
            'fields': ('date_created', 'date_updated')}),
    )
    readonly_fields = ('client', 'contract', 'date_created', 'date_updated')
    search_fields = ['contract', 'client']
    ordering = ['technician']
