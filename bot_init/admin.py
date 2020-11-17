from django.contrib import admin
from django.conf import settings

from bot_init.models import Message, Subscriber, AdminMessage


# TODO вынести действия в отдельный модуль
def activate_subscrbiers(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_subscrbiers.short_description = "Активировать пользвоателей"


def deactivate_subscrbiers(modeladmin, request, queryset):
    queryset.update(is_active=False)
activate_subscrbiers.short_description = "Деактивировать пользвоателей"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "chat_id", "text", "date")
    search_fields = ("text", "chat_id")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('tg_chat_id', 'is_active', 'registry_date', 'day')
    actions = [activate_subscrbiers, deactivate_subscrbiers]


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'text')

    def save_model(self, request, obj, form, change):
        obj.key = obj.key.lower().replace(' ', '_')
        obj.save()


if settings.DEBUG:
    admin.site.site_title = 'Тест. Iman game bot'
    admin.site.site_header = 'Тест. Iman game bot'
else:
    admin.site.site_title = 'Iman game bot. Панель управления'
    admin.site.site_header = 'Iman game bot. Панель управления'
