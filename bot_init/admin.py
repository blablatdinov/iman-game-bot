from django.contrib import admin

from bot_init.models import Message, Subscriber, AdminMessage


def activate_subscrbiers(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_subscrbiers.short_description = "Активировать пользвоателей"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "chat_id", "text")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('tg_chat_id', 'is_active')
    actions = [activate_subscrbiers]


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'text')

    def save_model(self, request, obj, form, change):
        obj.key = obj.key.lower().replace(' ', '_')
        obj.save()
