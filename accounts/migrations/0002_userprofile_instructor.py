# Generated by Django 5.1.4 on 2024-12-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='instructor',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
