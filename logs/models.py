from django.db import models


class Record(models.Model):
    """Модель записи лога"""

    ip = models.GenericIPAddressField('IP')
    date = models.DateField('Дата')
    http_method = models.CharField('Http метод', max_length=255)
    url = models.CharField('URL', max_length=255)
    answer_code = models.IntegerField('Код ответа')
    answer_size = models.IntegerField('Размер ответа')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Запись лога'
        verbose_name_plural = 'Записи логов'
