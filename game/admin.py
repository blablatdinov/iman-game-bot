from django.contrib import admin
from django.conf import settings

from game.models import MembersGroup


@admin.register(MembersGroup)
class MembersGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_link')

    def get_link(self, obj):
        return f'https://t.me/{settings.TG_BOT.name}?start=1'

    get_link.short_description = 'Ссылка'

