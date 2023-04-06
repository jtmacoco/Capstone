# Generated by Django 3.2.7 on 2023-04-05 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone_app', '0009_alter_portfolio_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='stocks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capstone_app.stock', unique=True),
        ),
    ]
