# Generated by Django 3.2.6 on 2021-09-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0003_auto_20210925_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userseminar',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]