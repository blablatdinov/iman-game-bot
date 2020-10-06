from django.contrib import admin
from django.conf import settings

from game.models import MembersGroup, DailyTask, RecordDailyTask


@admin.register(MembersGroup)
class MembersGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_link')
    fields = ('title', 'get_link')
    readonly_fields = ('get_link',)

    def get_link(self, obj):
        return f'https://t.me/{settings.TG_BOT.name}?start=1'

    get_link.short_description = 'Ссылка'


@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('task_type', 'text', 'week_day')


@admin.register(RecordDailyTask)
class RecordDailyTaskAdmin(admin.ModelAdmin):
    ...
    # list_display = ('task_type', 'text')