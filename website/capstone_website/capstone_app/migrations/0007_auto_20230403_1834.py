# Generated by Django 3.2.7 on 2023-04-03 18:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('capstone_app', '0006_portfolio_stocks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='stocks',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='stocks',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='capstone_app.stock'),
            preserve_default=False,
        ),
    ]
