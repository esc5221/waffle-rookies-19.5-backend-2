# Generated by Django 3.2.6 on 2021-09-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0002_userseminar_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userseminar',
            name='dropped_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userseminar',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userseminar',
            name='joined_at',
            field=models.DateTimeField(default='2021-09-25 08:34:03.284879'),
            preserve_default=False,
        ),
    ]