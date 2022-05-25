# Generated by Django 4.0.2 on 2022-05-24 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZadaraPods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('url_base', models.CharField(max_length=500)),
                ('pod_user', models.CharField(max_length=50)),
                ('pod_password', models.CharField(max_length=150)),
            ],
        ),
    ]
