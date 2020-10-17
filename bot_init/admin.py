from django.contrib import admin

from bot_init.models import Message, Subscriber, AdminMessage


admin.site.register(Message)
admin.site.register(Subscriber)


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'text')

    def save_model(self, request, obj, form, change):
        obj.key = obj.key.lower().replace(' ', '_')
        obj.save()
