from django.contrib import admin
from .models import Record


class RecordAdmin(admin.ModelAdmin):
    """Выводим состовляющие записей для админки"""

    list_display = ('id', 'ip', 'date', 'http_method', 'url', 'answer_code', 'answer_size', )


admin.site.register(Record, RecordAdmin)
