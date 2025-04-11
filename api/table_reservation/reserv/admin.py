from django.contrib import admin

from .models import *


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'seats', 'get_location_display']
    list_display_links = ['id', 'name', 'seats', 'get_location_display']

    def get_location_display(self, obj):
        return obj.get_location_display()

    get_location_display.short_description = 'Расположение'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'table_id', 'reservation_time', 'duration_minutes']
    list_display_links = ['id', 'customer_name', 'table_id', 'reservation_time', 'duration_minutes']
