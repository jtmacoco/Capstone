# Generated by Django 3.2.7 on 2023-04-03 18:22

from django.db import migrations, models
import django.db.models.deletion


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
            field=models.ForeignKey(default='test', on_delete=django.db.models.deletion.CASCADE, to='capstone_app.stock'),
        ),
    ]