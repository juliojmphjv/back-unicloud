# Generated by Django 4.0.7 on 2022-09-01 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unicloud_sales', '0004_calculator_measureunit_ratios_subscriptions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Calculator',
        ),
        migrations.DeleteModel(
            name='MeasureUnit',
        ),
        migrations.DeleteModel(
            name='Ratios',
        ),
        migrations.DeleteModel(
            name='Subscriptions',
        ),
    ]
