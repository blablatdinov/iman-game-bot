from django.contrib import admin

from bot_init.models import Message, Subscriber, AdminMessage


def activate_subscrbiers(modeladmin, request, queryset):
    queryset.update(status='p')
activate_subscrbiers.short_description = "Активировать пользвоателей"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "key")


admin.site.register(Subscriber)


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'text')

    def save_model(self, request, obj, form, change):
        obj.key = obj.key.lower().replace(' ', '_')
        obj.save()
