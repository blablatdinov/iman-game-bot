from django.contrib import admin

from bot_init.models import Message, Subscriber, AdminMessage


admin.site.register(Message)
admin.site.register(Subscriber)


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    ...
