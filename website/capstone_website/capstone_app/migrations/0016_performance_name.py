# Generated by Django 3.2.7 on 2023-04-19 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone_app', '0015_auto_20230417_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
