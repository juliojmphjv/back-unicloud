# Generated by Django 4.0.7 on 2022-09-06 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicloud_sales', '0009_alter_currencymodel_safety_margin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencymodel',
            name='currency',
            field=models.CharField(default='usd', max_length=5),
        ),
    ]
