from django.contrib import admin
from .models import Calendar, Event


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('modal_title', 'activate')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_of_event', 'calendar')


admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Event, EventAdmin)