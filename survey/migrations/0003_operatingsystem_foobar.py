from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_surveyresult_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='operatingsystem',
            name='foobar',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
