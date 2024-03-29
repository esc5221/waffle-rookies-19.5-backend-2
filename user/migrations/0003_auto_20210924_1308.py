# Generated by Django 3.2.6 on 2021-09-24 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='instructor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.instructorprofile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='participant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.participantprofile'),
        ),
    ]
