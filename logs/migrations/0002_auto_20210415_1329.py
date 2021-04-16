# Generated by Django 3.2 on 2021-04-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='answer_code',
            field=models.IntegerField(verbose_name='Код ответа'),
        ),
        migrations.AlterField(
            model_name='record',
            name='answer_size',
            field=models.IntegerField(verbose_name='Размер ответа'),
        ),
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='record',
            name='http_method',
            field=models.CharField(max_length=255, verbose_name='Http метод'),
        ),
        migrations.AlterField(
            model_name='record',
            name='ip',
            field=models.GenericIPAddressField(verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='record',
            name='url',
            field=models.CharField(max_length=255, verbose_name='URL'),
        ),
    ]