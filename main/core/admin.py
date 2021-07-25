from django.contrib import admin
from .models import (Account, Event_simple, Event_detailed)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Event_simple)
class Event_simpleAdmin(admin.ModelAdmin):
    pass

@admin.register(Event_detailed)
class Event_detailedAdmin(admin.ModelAdmin):
    pass