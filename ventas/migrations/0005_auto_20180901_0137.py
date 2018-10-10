# Generated by Django 2.1.1 on 2018-09-01 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_auto_20180901_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, choices=[('draft', 'Quotation'), ('sent', 'Quotation Sent'), ('sale', 'Sales Order'), ('done', 'Locked'), ('cancel', 'Cancelled')], editable=False, help_text='', max_length=512, null=True, verbose_name='Status'),
        ),
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
