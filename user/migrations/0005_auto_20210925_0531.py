# Generated by Django 3.2.6 on 2021-09-25 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210924_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructorprofile',
            name='company',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='university',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]