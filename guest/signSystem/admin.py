
from django.contrib import admin
from .models.event import Event
from .models.guest import Guest


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name']    # search bar
    list_filter = ['status']    # filter


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    list_display_links = ('realname', 'phone')  # show link
    search_fields = ['realname', 'phone']   # search bar
    list_filter = ['event_id']  # filter


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)