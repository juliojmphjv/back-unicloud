# Generated by Django 4.0.6 on 2022-07-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicloud_sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='opportunity_name',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]
