from PIL import Image
from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe

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
    list_display = ('task_type', 'text', 'week_day', 'get_image')

    def save_model(self, request, obj, *args):
        super().save_model(request, obj, *args)
        quality = 40
        foo = Image.open(obj.image.path)
        foo.save(obj.image.path, optimize=True, quality=quality)

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.image.url} width="50" height="50"')
        except ValueError:
            return mark_safe("Изображение не загружено")

    get_image.short_description = "Изображение"


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
    list_editable = ('is_done', 'is_selected')
    list_per_page = 300

    def task_type(self, obj):
        return obj.task.get_task_type_display()

    task_type.short_description = "Тип задания"


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
