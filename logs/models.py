from django.db import models


class Record(models.Model):
    """Модель записи лога"""

    ip = models.GenericIPAddressField('IP', null=True)
    date = models.DateField('Дата', null=True)
    http_method = models.CharField('Http метод', max_length=255, null=True)
    url = models.CharField('URL', max_length=255, null=True)
    answer_code = models.IntegerField('Код ответа', null=True)
    answer_size = models.IntegerField('Размер ответа', null=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Запись лога'
        verbose_name_plural = 'Записи логов'
