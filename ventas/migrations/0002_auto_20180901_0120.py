# Generated by Django 2.1.1 on 2018-09-01 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(default='', editable=False, help_text='', max_length=512, verbose_name='Order Reference'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(blank=True, help_text='', max_length=512, null=True, verbose_name='Name'),
        ),
    ]
