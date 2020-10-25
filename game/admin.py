from django.contrib import admin
from django.conf import settings

from game.models import MembersGroup, DailyTask, RecordDailyTask, BeginSurveyQuestion, Reminder


@admin.register(BeginSurveyQuestion)
class BeginSurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("type", "text")


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
    list_display = (
        "id",
        "subscriber",
        "task",
        "is_done",
        "is_selected",
        "date",
        "complexity",
        "task_type",
    )
    list_editable = ('is_done',)

    def get_queryset(self, request):
        return self.model.objects.filter(is_selected=True)

    def task_type(self, obj):
        return obj.task.get_task_type_display()

    task_type.short_description = "Тип задания"

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
